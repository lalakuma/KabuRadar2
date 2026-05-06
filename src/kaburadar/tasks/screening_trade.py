from __future__ import annotations

import argparse
from datetime import datetime


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["HI", "LO"])
    args = parser.parse_args()

    print(f"[{datetime.now().isoformat()}] screening_trade({args.mode}): started")
    print("TODO: migrate param change, analyze, and trade flow.")
    print(f"screening_trade({args.mode}): completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
