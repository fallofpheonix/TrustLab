from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any

from storage.base import BaseStore


class SQLiteStore(BaseStore):
    """SQLite-backed event store for environments requiring stronger durability."""

    FIELDNAMES = [
        "participant_id",
        "condition_id",
        "assistant_name",
        "assistant_tone",
        "confidence_frame",
        "decision",
        "decision_matches_recommendation",
        "recommendation_id",
        "recommended_option",
        "timestamp",
        "latency_ms",
        "user_agent",
    ]

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        participant_id TEXT NOT NULL,
        condition_id TEXT NOT NULL,
        assistant_name TEXT,
        assistant_tone TEXT,
        confidence_frame TEXT,
        decision TEXT NOT NULL,
        decision_matches_recommendation TEXT,
        recommendation_id TEXT,
        recommended_option TEXT,
        timestamp TEXT NOT NULL,
        latency_ms INTEGER,
        user_agent TEXT,
        raw_json TEXT
    )
    """

    def __init__(self, db_path: Path) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path
        self._lock = threading.Lock()
        # Initialize schema on a single connection; subsequent operations
        # each open their own connection to avoid cross-thread sharing.
        with sqlite3.connect(str(db_path)) as conn:
            conn.execute(self._CREATE_TABLE)
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self._db_path))

    def append(self, event: dict[str, Any]) -> None:
        row = [event.get(k, "") for k in self.FIELDNAMES]
        placeholders = ", ".join("?" for _ in self.FIELDNAMES)
        cols = ", ".join(self.FIELDNAMES)
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    f"INSERT INTO events ({cols}, raw_json) VALUES ({placeholders}, ?)",
                    row + [json.dumps(event)],
                )
                conn.commit()

    def all_events(self) -> list[dict[str, Any]]:
        cols = ", ".join(self.FIELDNAMES)
        with self._connect() as conn:
            cur = conn.execute(f"SELECT {cols} FROM events ORDER BY id")
            return [dict(zip(self.FIELDNAMES, row)) for row in cur.fetchall()]

    def event_count(self) -> int:
        with self._connect() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM events")
            return cur.fetchone()[0]
