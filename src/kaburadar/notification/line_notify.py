from __future__ import annotations

import os
from datetime import datetime
from typing import Iterable

import requests
from dotenv import load_dotenv


def _get_env() -> tuple[str, list[str]]:
    load_dotenv()
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
    users = [x.strip() for x in os.getenv("LINE_USER_IDS", "").split(",") if x.strip()]
    return token, users


def notify(codes: Iterable[str], stance: str) -> bool:
    # Do not notify on weekend.
    if datetime.today().isoweekday() in [6, 7]:
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
