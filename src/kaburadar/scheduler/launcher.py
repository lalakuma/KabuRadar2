"""後方互換: scheduler → scheduling."""

from kaburadar.scheduling.launcher import run_for_now

__all__ = ["run_for_now"]

if __name__ == "__main__":
    run_for_now()
