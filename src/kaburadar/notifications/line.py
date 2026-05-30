from __future__ import annotations

import os
from datetime import datetime
from typing import Iterable

import requests

try:
    from dotenv import load_dotenv
except Exception:  # noqa: BLE001
    def load_dotenv(*_args, **_kwargs):  # type: ignore[no-redef]
        return False


def _get_env() -> tuple[str, list[str]]:
    load_dotenv()
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
    users = [x.strip() for x in os.getenv("LINE_USER_IDS", "").split(",") if x.strip()]
    return token, users


def is_configured() -> bool:
    token, users = _get_env()
    return bool(token and users and token != "change_me")


def is_weekend() -> bool:
    return datetime.today().isoweekday() in (6, 7)


def notify(codes: Iterable[str], stance: str) -> bool:
    if is_weekend():
        return False

    token, users = _get_env()
    if not token or not users:
        raise RuntimeError("LINE settings are not configured in .env")

    message = "\n".join(codes) if codes else "not found"
    full_message = f"{stance} {message}".strip()

    response = requests.post(
        "https://api.line.me/v2/bot/message/multicast",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"to": users, "messages": [{"type": "text", "text": full_message}]},
        timeout=15,
    )
    response.raise_for_status()
    return True


def notify_optional(codes: Iterable[str], stance: str) -> bool:
    """未設定・週末のときは例外にせずスキップする（個人運用向け）。"""
    if is_weekend():
        print("LINE: 週末のため送信しません。")
        return False
    if not is_configured():
        print("LINE: .env 未設定のため送信しません。")
        return False
    try:
        return notify(codes, stance)
    except Exception as exc:  # noqa: BLE001
        print(f"LINE: 送信失敗 ({exc})")
        return False


def notify_analysis_summary(stance: str = "LO", limit: int = 10) -> bool:
    """最新集計 CSV から上位銘柄を LINE 送信する。"""
    from kaburadar.notifications.summary import format_summary_header, format_top_symbols

    lines = format_top_symbols(limit=limit)
    if not lines:
        print("LINE: 集計 CSV がないため送信しません。")
        return False
    header = format_summary_header()
    body = [header] if header else []
    body.extend(lines)
    return notify_optional(body, stance)
