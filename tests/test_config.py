from __future__ import annotations

from pathlib import Path

from kaburadar.config import CONFIG_LO, PROJECT_ROOT, read_config, resolve_path_value


def test_config_lo_exists() -> None:
    assert CONFIG_LO.exists()


def test_read_screening_rsi4() -> None:
    assert read_config("SCREENING", "SCR_JDG_RSI4", config_path=CONFIG_LO) == "1"


def test_resolve_path_db() -> None:
    raw = read_config("DATABASE", "PATH_DB", config_path=CONFIG_LO)
    path = resolve_path_value(raw)
    assert path == (PROJECT_ROOT / "data" / "kaburadar.db").resolve()


def test_no_config_hi() -> None:
    assert not (PROJECT_ROOT / "config" / "config_hi.ini").exists()
