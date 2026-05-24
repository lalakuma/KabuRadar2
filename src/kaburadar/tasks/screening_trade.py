from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[2]
TASKS_DIR = Path(__file__).resolve().parent


def _run_script(script: Path, *args: str) -> int:
    cmd = [sys.executable, str(script), *args]
    completed = subprocess.run(cmd, cwd=str(SRC_DIR.parents[1]))
    return int(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        nargs="?",
        default="LO",
        choices=["HI", "LO"],
        help="互換用。analyze は常に config_lo.ini を使用します。",
    )
    args = parser.parse_args()

    print(f"[{datetime.now().isoformat()}] screening_trade({args.mode}): started")

    rc = _run_script(TASKS_DIR / "analyze_all.py")
    if rc != 0:
        print(f"screening_trade: analyze_all failed with code {rc}")
        return rc

    print("TODO: migrate kabustation_trade flow.")
    print(f"screening_trade({args.mode}): completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
