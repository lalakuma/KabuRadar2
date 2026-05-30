"""解析結果 (output/honban) を GitHub Pages 用 docs/data.json に書き出す."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
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


def publish() -> dict:
    payload = build_payload()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Published: {DATA_FILE}")
    print(f"  symbols: {payload['summary']['symbol_count']}")
    print(f"  win_rate: {payload['summary'].get('win_rate')}%")
    return payload


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def push_to_github(payload: dict) -> int:
    """docs/data.json を commit して origin/master へ push する。"""
    add = _run_git(["add", "docs/data.json"])
    if add.returncode != 0:
        print(add.stderr or add.stdout)
        return add.returncode

    diff = _run_git(["diff", "--cached", "--quiet", "docs/data.json"])
    if diff.returncode == 0:
        print("変更なし: push をスキップしました。")
        return 0

    win_rate = payload["summary"].get("win_rate")
    income = payload["summary"].get("total_income")
    msg = f"解析結果を更新 (勝率 {win_rate}%, 損益 {income})"
    commit = _run_git(["commit", "-m", msg])
    if commit.returncode != 0:
        print(commit.stderr or commit.stdout)
        return commit.returncode

    push = _run_git(["push", "origin", "master"])
    if push.returncode != 0:
        print(push.stderr or push.stdout)
        print("push に失敗しました。git の認証設定を確認してください。")
        return push.returncode

    print("GitHub へ push 完了。1〜2分後に Pages が更新されます。")
    print("https://lalakuma.github.io/KabuRadar2/")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="解析結果を GitHub Pages 用 JSON に書き出す")
    parser.add_argument(
        "--push",
        action="store_true",
        help="docs/data.json を commit して origin/master へ push する",
    )
    args = parser.parse_args()

    payload = publish()
    if args.push:
        return push_to_github(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
