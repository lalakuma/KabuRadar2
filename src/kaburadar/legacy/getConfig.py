# coding: utf-8
"""Compatibility shim: original getConfig API backed by kaburadar.config (config_lo.ini)."""

from __future__ import annotations

import errno
import os
import shutil
from pathlib import Path

from kaburadar.config import CONFIG_LO, read_config, resolve_path_value

# Section names
CONF_SEC_SCR = "SCREENING"
CONF_SEC_SHUUKEI = "SHUUKEI"
CONF_SEC_ENTRY = "ENTRY"
CONF_SEC_KABUSAPI = "KABUSAPI"
CONF_SEC_DATABASE = "DATABASE"

# Keys (subset used by analyze / backtest / shuukei)
CONF_KEY_JDG_CAND = "SCR_JDG_CAND"
CONF_KEY_JDG_IND = "SCR_JDG_IND"
CONF_KEY_JDG_MOV = "SCR_JDG_MOV"
CONF_KEY_JDG_MOV_LONG = "SCR_JDG_MOV_LONG"
CONF_KEY_JDG_MOV_PFCT = "SCR_JDG_MOV_PFCT"
CONF_KEY_JDG_MOV_PUSH = "SCR_JDG_MOV_PUSH"
CONF_KEY_JDG_RSI = "SCR_JDG_RSI"
CONF_KEY_JDG_RSI4 = "SCR_JDG_RSI4"
CONF_KEY_JDG_RSI4REV = "SCR_JDG_RSI4REV"
CONF_KEY_JDG_BOLIN = "SCR_JDG_BOLIN"
CONF_KEY_JDG_MACD = "SCR_JDG_MACD"
CONF_KEY_JDG_BRK = "SCR_JDG_BRK"
CONF_KEY_JDG_BERD = "SCR_JDG_BERD"
CONF_KEY_JDG_BOTTOM = "SCR_JDG_BOTTOM"
CONF_KEY_JDG_RSVENT = "SCR_JDG_RSVENT"
CONF_KEY_JDG_3DAY = "SCR_JDG_3DAY"

CONF_KEY_SCR_SELLBUY = "SCR_SELLBUY"
CONF_KEY_SCR_ENT_TIMING = "SCR_ENT_TIMING"
CONF_KEY_SCR_EXEC_MODE = "SCR_EXEC_MODE"
CONF_KEY_SCR_PAST_PERIOD = "SCR_PAST_PERIOD"
CONF_KEY_SCR_SELL_PERIOD = "SCR_SELL_PERIOD"
CONF_KEY_SCR_BREAK_PERIOD = "SCR_BREAK_PERIOD"
CONF_KEY_SCR_BREAK_OFSET = "SCR_BREAK_OFSET"
CONF_KEY_SCR_MACD_OFSET = "SCR_MACD_OFSET"
CONF_KEY_SCR_LINEAVE = "SCR_LINEAVE"
CONF_KEY_SCR_RSI_MAX = "SCR_RSI_MAX"
CONF_KEY_SCR_RSI_BORDER = "SCR_RSI_BORDER"
CONF_KEY_SCR_RSI_PER = "SCR_RSI_PER"
CONF_KEY_SCR_RSI_PERIOD = "SCR_RSI_PERIOD"
CONF_KEY_SCR_SRSI_HI = "SCR_SRSI_HI"
CONF_KEY_SCR_SRSI_LOW = "SCR_SRSI_LOW"
CONF_KEY_SCR_IND_CODE = "SCR_IND_CODE"
CONF_KEY_SCR_ENTRY_REST = "SCR_ENTRY_REST"
CONF_KEY_PATH_SHUUKEI = "PATH_SHUUKEI"
CONF_KEY_PATH_HONBAN = "PATH_HONBAN"
CONF_KEY_PATH_CODESET = "PATH_CODESET"
CONF_KEY_PATH_DB = "PATH_DB"
CONF_KEY_API_PASSWD = "API_PASSWD"
CONF_KEY_TRD_PASSWD = "TRD_PASSWD"

_PATH_KEYS = frozenset(
    {
        CONF_KEY_PATH_SHUUKEI,
        CONF_KEY_PATH_HONBAN,
        CONF_KEY_PATH_CODESET,
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


def get_codeset_path() -> str:
    return get_config(CONF_SEC_ENTRY, CONF_KEY_PATH_CODESET)
