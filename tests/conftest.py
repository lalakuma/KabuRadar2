from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pytest


def _create_minimal_db(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, isolation_level=None)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS tbl_1000")
    cur.execute("DROP TABLE IF EXISTS tbl_codelist")
    cur.execute("DROP TABLE IF EXISTS tbl_code_set")
    cur.execute(
        'CREATE TABLE tbl_codelist (Code TEXT, name TEXT, col2 TEXT, sangyou TEXT)'
    )
    cur.execute(
        'INSERT INTO tbl_codelist VALUES ("1000", "テスト銘柄", "", "テスト業")'
    )
    cur.execute("CREATE TABLE tbl_code_set (code TEXT, Enable INTEGER)")
    cur.execute('INSERT INTO tbl_code_set VALUES ("1000", 1)')
    cur.execute(
        """CREATE TABLE tbl_1000 (
            datetime TEXT, open INTEGER, high INTEGER, low INTEGER,
            close INTEGER, volume INTEGER
        )"""
    )
    today = date.today()
    for i in range(45):
        d = today - timedelta(days=45 - i)
        price = 1000 + i * 5
        cur.execute(
            "INSERT INTO tbl_1000 VALUES (?,?,?,?,?,?)",
            (str(d), price, price + 5, price - 5, price, 10000),
        )
    conn.commit()
    conn.close()


@pytest.fixture
def minimal_db_path(tmp_path: Path) -> Path:
    db = tmp_path / "minimal.db"
    _create_minimal_db(db)
    return db
