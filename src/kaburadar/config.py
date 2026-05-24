from __future__ import annotations

import configparser
import os
import shutil
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except Exception:  # noqa: BLE001
    def load_dotenv(*_args, **_kwargs):  # type: ignore[no-redef]
        return False


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_HI = CONFIG_DIR / "config_hi.ini"
DEFAULT_LO = CONFIG_DIR / "config_lo.ini"
CONFIG_LO = DEFAULT_LO

_PATH_KEYS = frozenset(
    {
        "PATH_SHUUKEI",
        "PATH_HONBAN",
        "PATH_CODESET",
        "PATH_DB",
    }
)


def _load_env() -> None:
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        load_dotenv(env_file)


def _resolve_config_file(config_path: Optional[Path] = None) -> Path:
    if config_path is not None:
        return config_path
    if CONFIG_LO.exists():
        return CONFIG_LO
    if DEFAULT_HI.exists():
        return DEFAULT_HI
    raise FileNotFoundError(f"No config file found in: {CONFIG_DIR}")


def resolve_path_value(raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return (PROJECT_ROOT / candidate).resolve()


def read_path_config(section: str, key: str, config_path: Optional[Path] = None) -> Path:
    return resolve_path_value(read_config(section, key, config_path=config_path))


def copy_config_snapshot(dest_dir: Path, config_path: Optional[Path] = None) -> None:
    src = _resolve_config_file(config_path)
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dest_dir / src.name)


def read_config(section: str, key: str, config_path: Optional[Path] = None) -> str:
    _load_env()
    parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    parser.read(_resolve_config_file(config_path), encoding="utf-8")
    value = parser.get(section, key)

    # Allow environment overrides for secrets.
    if value.startswith("${") and value.endswith("}"):
        env_key = value[2:-1]
        return os.getenv(env_key, "")
    return value


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)
