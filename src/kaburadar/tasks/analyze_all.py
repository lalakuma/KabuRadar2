from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[2]
LEGACY_DIR = SRC_DIR / "kaburadar" / "legacy"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(LEGACY_DIR) not in sys.path:
    sys.path.insert(0, str(LEGACY_DIR))

import backtest_proc as bktst  # noqa: E402
import getConfig as conf  # noqa: E402
import main_write_shuukei_csv as shuukei  # noqa: E402
import sqlight as db  # noqa: E402

from kaburadar.config import CONFIG_LO, PROJECT_ROOT, copy_config_snapshot  # noqa: E402

STANCE = "LO"
LOG_DIR = PROJECT_ROOT / "output" / "log"


def _setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("kaburadar.analyze_all")
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


def _write_csv(dt: bktst.KabInf, kekka_path: str, code: str, coderec) -> None:
    if not dt.outcodecsv:
        return
    winrate = bktst.KabInf.get_winrate(dt)
    wlstr = (
        "_rsi"
        + str(dt.adopt_rsi)
        + "_W"
        + str(dt.win)
        + "L"
        + str(dt.lose)
        + "_"
        + str(winrate)
        + "%_YEN"
        + str(dt.income)
        + "_PF"
        + str(dt.pf)
        + "_pg"
        + str(dt.plusgain)
        + "_mg"
        + str(dt.minusgain)
        + "_"
        + coderec[0].replace("\uff0d", "-")
        + "_"
        + coderec[1].replace("\uff0d", "-")
        + "_"
    )
    out_path = os.path.join(kekka_path, f"code{code}{wlstr}.csv")
    dt.outdf.to_csv(out_path, encoding="shift_jis")


def _prepare_output_dir(kekka_path: str) -> None:
    path = Path(kekka_path)
    path.mkdir(parents=True, exist_ok=True)
    for csv_file in path.glob("*.csv"):
        csv_file.unlink()
    summary = path / f"集計_{STANCE}.xlsx"
    if summary.exists():
        summary.unlink()


def _build_kab_inf(scrsec: str, past_period: int) -> bktst.KabInf:
    return bktst.KabInf(
        sell_period=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_SELL_PERIOD)),
        breakout=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_BREAK_PERIOD)),
        break_offset=float(conf.get_config(scrsec, conf.CONF_KEY_SCR_BREAK_OFSET)),
        macd_offset=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_MACD_OFSET)),
        lineave=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_LINEAVE)),
        past_period=past_period,
        rsi_period=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_RSI_PERIOD)),
        rsi_border=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_RSI_BORDER)),
        rsi_max=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_RSI_MAX)),
        rsi_per=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_RSI_PER)),
        srsi_hi=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_SRSI_HI)),
        srsi_low=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_SRSI_LOW)),
        ent_rest=int(conf.get_config(scrsec, conf.CONF_KEY_SCR_ENTRY_REST)),
    )


def run() -> int:
    logger = _setup_logger()
    logger.info("処理 analyze_all を低勝率高回転モード(config_lo.ini)で開始します。")

    conn, cursor = db.connect_db()
    try:
        codes = db.read_code_all(cursor, "tbl_codelist")
        scrsec = conf.CONF_SEC_SCR
        past_period = int(conf.get_config(scrsec, conf.CONF_KEY_SCR_PAST_PERIOD)) * (-1)

        cls_dt = _build_kab_inf(scrsec, past_period)
        kekka_path = conf.get_config(conf.CONF_SEC_SHUUKEI, conf.CONF_KEY_PATH_HONBAN)

        _prepare_output_dir(kekka_path)
        cls_dt.write_prm_tocsv(kekka_path)
        copy_config_snapshot(Path(kekka_path), config_path=CONFIG_LO)

        df_indicator = pd.DataFrame()
        df_set = db.read_rec_all(conn, cursor, "tbl_code_set")
        df_set = df_set.set_index("code")

        for code in codes:
            print("CODE=", code)
            if df_set.at[str(code), "Enable"] == 0:
                continue

            result = bktst.backtst_proc(code, df_indicator, cls_dt, conn, cursor)
            if result == -1:
                continue

            coderec = db.read_code_record(cursor, cursor, code)
            _write_csv(cls_dt, kekka_path, str(code), coderec)

        fullpath_shuukei = shuukei.shuukei_toCsv(kekka_path)
        _shuukei, _filepath, final_rieki = shuukei.shuukei_makeExl(kekka_path, STANCE)

        if fullpath_shuukei:
            newfilename = fullpath_shuukei.replace("PF", f"Y{final_rieki}_PF")
            os.rename(fullpath_shuukei, newfilename)

        logger.info("処理 analyze_all を完了しました。")
        return 0
    finally:
        db.close_db(conn)


def main() -> int:
    parser = argparse.ArgumentParser(description="全銘柄バックテスト解析 (config_lo.ini)")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="完了後に GitHub Pages 用 JSON を生成し push する",
    )
    args = parser.parse_args()

    rc = run()
    if rc != 0 or not args.publish:
        return rc

    import subprocess

    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "publish_results.py"), "--push"]
    completed = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
