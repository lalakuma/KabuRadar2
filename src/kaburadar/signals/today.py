"""解析結果 CSV から当日の買い・返売りシグナルを抽出."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from kaburadar.settings.encoding import read_csv

MARK_NEW_BUY = "新買"
MARK_SELLBACK = "返売"
_CODE_CSV = re.compile(r"^code(\d+)", re.IGNORECASE)


def _row_trade_date(row: pd.Series, idx: object) -> pd.Timestamp | None:
    if "Index" in row.index and pd.notna(row["Index"]):
        return pd.Timestamp(row["Index"]).normalize()
    if isinstance(idx, pd.Timestamp):
        return idx.normalize()
    return None


def _read_code_marks(path: Path) -> list[tuple[str, pd.Timestamp, str, float | None]]:
    """(code, date, mark, close) のリスト。"""
    df = read_csv(path)
    if df.empty or "mark" not in df.columns:
        return []
    match = _CODE_CSV.match(path.name)
    if not match:
        return []
    code = match.group(1)
    rows: list[tuple[str, pd.Timestamp, str, float | None]] = []
    for idx, row in df.iterrows():
        mark = str(row.get("mark", "")).strip()
        if mark not in (MARK_NEW_BUY, MARK_SELLBACK):
            continue
        dt = _row_trade_date(row, idx)
        if dt is None:
            continue
        close_val = row.get("close")
        close = float(close_val) if pd.notna(close_val) else None
        rows.append((code, dt, mark, close))
    return rows


def collect_today_signals(
    results_dir: Path,
    name_map: dict[str, str] | None = None,
) -> dict:
    """最新営業日の新買・返売りを返す。"""
    name_map = name_map or {}
    all_rows: list[tuple[str, pd.Timestamp, str, float | None]] = []
    for path in sorted(results_dir.glob("code*.csv")):
        all_rows.extend(_read_code_marks(path))

    if not all_rows:
        return {
            "trade_date": None,
            "new_buy": [],
            "sellback": [],
            "new_buy_count": 0,
        }

    trade_date = max(dt for _c, dt, _m, _cl in all_rows)
    trade_str = trade_date.strftime("%Y-%m-%d")

    def _to_item(code: str, mark: str, close: float | None) -> dict:
        item = {
            "code": code,
            "name": name_map.get(code, ""),
            "mark": mark,
        }
        if close is not None:
            item["close"] = int(round(close))
        return item

    new_buy: list[dict] = []
    sellback: list[dict] = []
    for code, dt, mark, close in all_rows:
        if dt != trade_date:
            continue
        if mark == MARK_NEW_BUY:
            new_buy.append(_to_item(code, mark, close))
        elif mark == MARK_SELLBACK:
            sellback.append(_to_item(code, mark, close))

    new_buy.sort(key=lambda x: x["code"])
    sellback.sort(key=lambda x: x["code"])
    return {
        "trade_date": trade_str,
        "new_buy": new_buy,
        "sellback": sellback,
        "new_buy_count": len(new_buy),
    }
