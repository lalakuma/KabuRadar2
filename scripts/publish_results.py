"""解析結果 (output/honban) を GitHub Pages 用 docs/data.json に書き出す."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HONBAN_DIR = PROJECT_ROOT / "output" / "honban"
DOCS_DIR = PROJECT_ROOT / "docs"
DATA_FILE = DOCS_DIR / "data.json"


def _find_summary_csv(directory: Path) -> Path | None:
    candidates = sorted(directory.glob("Y*_PF*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def _parse_summary_filename(path: Path) -> dict:
    name = path.stem
    match = re.search(
        r"Y\d+_PF([\d.]+)_W(\d+)L(\d+)_rate([\d.]+)_all(\d+)",
        name,
    )
    if not match:
        return {}
    return {
        "pf": float(match.group(1)),
        "wins": int(match.group(2)),
        "losses": int(match.group(3)),
        "win_rate": float(match.group(4)),
        "total_income": int(match.group(5)),
    }


def _load_symbols(summary_csv: Path) -> list[dict]:
    df = pd.read_csv(summary_csv, encoding="shift_jis")
    rows: list[dict] = []
    for _, row in df.iterrows():
        rows.append(
            {
                "code": str(row.get("code", "")),
                "name": str(row.get("name", "")),
                "industry": str(row.get("sangyou", "")),
                "incomes": int(row.get("incomes", 0) or 0),
                "pf": float(row.get("pf", 0) or 0),
                "winlose": str(row.get("winlose", "")),
                "win_per": int(row.get("winPer", 0) or 0),
                "plus_gain": int(row.get("pg", 0) or 0),
                "minus_gain": int(row.get("mg", 0) or 0),
            }
        )
    rows.sort(key=lambda r: r["incomes"], reverse=True)
    return rows


def build_payload() -> dict:
    if not HONBAN_DIR.is_dir():
        raise FileNotFoundError(f"結果フォルダがありません: {HONBAN_DIR}")

    summary_csv = _find_summary_csv(HONBAN_DIR)
    if summary_csv is None:
        raise FileNotFoundError(f"集計 CSV (Y*_PF*.csv) が見つかりません: {HONBAN_DIR}")

    symbols = _load_symbols(summary_csv)
    meta = _parse_summary_filename(summary_csv)
    wins = sum(1 for s in symbols if "W1" in s["winlose"] or "W2" in s["winlose"])
    losses = sum(1 for s in symbols if "L1" in s["winlose"])
    neutral = sum(1 for s in symbols if s["winlose"] == "W0L0")

    return {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "mode": "LO",
        "summary": {
            "pf": meta.get("pf"),
            "wins": meta.get("wins", wins),
            "losses": meta.get("losses", losses),
            "win_rate": meta.get("win_rate"),
            "total_income": meta.get("total_income", sum(s["incomes"] for s in symbols)),
            "symbol_count": len(symbols),
            "neutral_count": neutral,
            "source_file": summary_csv.name,
        },
        "symbols": symbols,
    }


def main() -> int:
    payload = build_payload()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Published: {DATA_FILE}")
    print(f"  symbols: {payload['summary']['symbol_count']}")
    print(f"  win_rate: {payload['summary'].get('win_rate')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
