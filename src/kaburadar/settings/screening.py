"""SCREENING / SHUUKEI セクション向けのレガシー互換 API."""

from __future__ import annotations

import errno
import os
import shutil
from pathlib import Path

from .loader import read_config, resolve_path_value
from .paths import CONFIG_LO

CONF_SEC_SCR = "SCREENING"
CONF_SEC_SHUUKEI = "SHUUKEI"
CONF_SEC_DATABASE = "DATABASE"

CONF_KEY_JDG_RSI4 = "SCR_JDG_RSI4"
CONF_KEY_JDG_RSI4REV = "SCR_JDG_RSI4REV"
CONF_KEY_JDG_RSVENT = "SCR_JDG_RSVENT"

CONF_KEY_SCR_SELLBUY = "SCR_SELLBUY"
CONF_KEY_SCR_ENT_TIMING = "SCR_ENT_TIMING"
CONF_KEY_SCR_PAST_PERIOD = "SCR_PAST_PERIOD"
CONF_KEY_SCR_SELL_PERIOD = "SCR_SELL_PERIOD"
CONF_KEY_SCR_RSI_MAX = "SCR_RSI_MAX"
CONF_KEY_SCR_RSI_BORDER = "SCR_RSI_BORDER"
CONF_KEY_SCR_RSI_PER = "SCR_RSI_PER"
CONF_KEY_SCR_RSI_PERIOD = "SCR_RSI_PERIOD"
CONF_KEY_SCR_SRSI_HI = "SCR_SRSI_HI"
CONF_KEY_SCR_SRSI_LOW = "SCR_SRSI_LOW"
CONF_KEY_SCR_ENTRY_REST = "SCR_ENTRY_REST"
CONF_KEY_PATH_SHUUKEI = "PATH_SHUUKEI"
CONF_KEY_PATH_HONBAN = "PATH_HONBAN"
CONF_KEY_PATH_DB = "PATH_DB"

_PATH_KEYS = frozenset(
    {
        CONF_KEY_PATH_SHUUKEI,
        CONF_KEY_PATH_HONBAN,
        CONF_KEY_PATH_DB,
    }
)


def _as_legacy_dir(path: Path) -> str:
    text = str(path)
    if not text.endswith(("\\", "/")):
        text += os.sep
    return text


def get_confFilePath() -> str:
    return str(CONFIG_LO)


def get_config(section: str, key: str) -> str:
    if not CONFIG_LO.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(CONFIG_LO))
    raw = read_config(section, key, config_path=CONFIG_LO)
    if key in _PATH_KEYS:
        resolved = resolve_path_value(raw)
        if key == CONF_KEY_PATH_DB:
            return str(resolved)
        return _as_legacy_dir(resolved)
    return raw


def copy_confFile(destpath: str) -> None:
    if not CONFIG_LO.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(CONFIG_LO))
    dest = Path(destpath)
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy(CONFIG_LO, dest / CONFIG_LO.name)
