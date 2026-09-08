"""Small, read-only friendly SQLite access layer."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable


class SQLiteDatabase:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def connect(self) -> sqlite3.Connection:
        if not self.path.exists():
            raise FileNotFoundError(f"database not found: {self.path}")
        con = sqlite3.connect(self.path, timeout=10)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA query_only = ON")
        con.execute("PRAGMA busy_timeout = 10000")
        return con

    def execute(self, sql: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
        with self.connect() as con:
            cur = con.execute(sql, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    def health(self) -> bool:
        try:
            return self.execute("SELECT 1 AS ok") == [{"ok": 1}]
        except (OSError, sqlite3.Error):
            return False
