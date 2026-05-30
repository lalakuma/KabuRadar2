from __future__ import annotations

import datetime as dt
import logging

from kaburadar.settings.paths import LOG_DIR
from kaburadar.settings.scripts import run_script, script_path

SCREENING = "screening"
UPDATE_PRICES = "update_prices"


def _setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("kaburadar.scheduling")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    fh = logging.FileHandler(LOG_DIR / "debug.log", encoding="utf-8")
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger


def _run_task(candidates: list[str], logger: logging.Logger) -> None:
    for name in candidates:
        path = script_path(name)
        if path.is_file():
            logger.info("Run script: %s", path)
            run_script(name)
            return
    logger.warning("No script found from candidates: %s", candidates)


def run_for_now(now: dt.datetime | None = None) -> None:
    logger = _setup_logger()
    now = now or dt.datetime.now()
    tm = now.time()
    logger.info("Launcher started at %s", now.isoformat())

    if dt.time(11, 30, 0) <= tm <= dt.time(12, 0, 0):
        _run_task([SCREENING], logger)
        return

    if dt.time(9, 0, 0) <= tm <= dt.time(14, 30, 0):
        _run_task([SCREENING], logger)
        return

    if dt.time(15, 0, 0) <= tm <= dt.time(15, 30, 0):
        _run_task([UPDATE_PRICES], logger)
        return

    logger.info("No matching execution window. Nothing executed.")


if __name__ == "__main__":
    run_for_now()
