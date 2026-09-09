"""Sidecar SQLite store for reviewed query feedback."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FeedbackStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS query_feedback (
                    query_id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    final_sql TEXT NOT NULL,
                    confidence TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    rating TEXT CHECK (rating IN ('correct', 'incorrect')),
                    comment TEXT,
                    feedback_updated_at TEXT
                )
                """
            )

    def record_query(self, payload: dict[str, Any]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO query_feedback
                    (query_id, question, final_sql, confidence, attempt_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["query_id"],
                    payload["question"],
                    payload["sql"],
                    payload["confidence"],
                    payload["attempt_count"],
                    now,
                ),
            )

    def save_feedback(self, query_id: str, rating: str, comment: str | None = None) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE query_feedback
                SET rating = ?, comment = ?, feedback_updated_at = ?
                WHERE query_id = ?
                """,
                (rating, comment or None, now, query_id),
            )
            return cursor.rowcount == 1

    def get(self, query_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM query_feedback WHERE query_id = ?", (query_id,)
            ).fetchone()
            return dict(row) if row else None
