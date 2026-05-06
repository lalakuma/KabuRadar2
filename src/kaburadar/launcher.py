from __future__ import annotations

import datetime as dt
import logging
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BAT_DIR = ROOT / "bat"
LOG_DIR = ROOT / "output" / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _setup_logger() -> logging.Logger:
    logger = logging.getLogger("kaburadar.launcher")
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


def _run_bat(candidates: list[str], logger: logging.Logger) -> None:
    for name in candidates:
        path = BAT_DIR / name
        if path.exists():
            logger.info("Run batch: %s", path)
            subprocess.run([str(path)], check=False, cwd=str(BAT_DIR), shell=True)
            return
    logger.warning("No batch file found from candidates: %s", candidates)


def run_for_now(now: dt.datetime | None = None) -> None:
    logger = _setup_logger()
    now = now or dt.datetime.now()
    tm = now.time()
    logger.info("Launcher started at %s", now.isoformat())

    if dt.time(8, 45, 0) <= tm <= dt.time(9, 30, 0):
        _run_bat(["1-1.kabu_yori_arugo.bat"], logger)
        return

    if dt.time(11, 30, 0) <= tm <= dt.time(12, 0, 0):
        _run_bat(["2-1.kabu_screening_trade.bat", "2-1.kabu_screening_trade_GetYahooF.bat"], logger)
        return

    if dt.time(9, 0, 0) <= tm <= dt.time(14, 30, 0):
        _run_bat(["2-2.KabuStation_kessai.bat", "2-2.KabuStation_kessai_GetYahooF.bat"], logger)
        return

    if dt.time(15, 0, 0) <= tm <= dt.time(15, 30, 0):
        _run_bat(["2-3.GetKabuka.bat", "2-3.GetKabuka_GetYahooF.bat"], logger)
        return

    logger.info("No matching execution window. Nothing executed.")


if __name__ == "__main__":
    run_for_now()
