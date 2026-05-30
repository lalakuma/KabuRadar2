"""集計 CSV から LINE 用の短いサマリーを作る."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from kaburadar.settings.encoding import read_csv
from kaburadar.settings.loader import read_path_config


def _find_summary_csv(directory: Path) -> Path | None:
    candidates = sorted(directory.glob("Y*_PF*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def format_top_symbols(limit: int = 10, results_dir: Path | None = None) -> list[str]:
    """損益上位銘柄を「コード 銘柄名 損益」形式の行リストで返す。"""
    if results_dir is None:
        results_dir = read_path_config("SHUUKEI", "PATH_HONBAN")
    summary_csv = _find_summary_csv(results_dir)
    if summary_csv is None:
        return []

    df = read_csv(summary_csv)
    if df.empty:
        return []

    df = df.sort_values("incomes", ascending=False).head(limit)
    lines: list[str] = []
    for _, row in df.iterrows():
        code = str(row.get("code", ""))
        name = str(row.get("name", ""))
        incomes = int(row.get("incomes", 0) or 0)
        wl = str(row.get("winlose", ""))
        lines.append(f"{code} {name} ¥{incomes:,d} ({wl})")
    return lines


def format_summary_header(results_dir: Path | None = None) -> str:
    """集計ファイル名から PF・勝率の一行ヘッダーを返す。"""
    if results_dir is None:
        results_dir = read_path_config("SHUUKEI", "PATH_HONBAN")
    summary_csv = _find_summary_csv(results_dir)
    if summary_csv is None:
        return ""
    return summary_csv.stem.replace("_", " ")
