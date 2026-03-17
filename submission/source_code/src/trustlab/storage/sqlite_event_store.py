from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any

from trustlab.storage.atomic_event_logger import EVENT_FIELDS
from trustlab.storage.base import EventStore


class SQLiteEventStore(EventStore):
    _CREATE_SQL = """
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
        with sqlite3.connect(str(self._db_path)) as connection:
            connection.execute(self._CREATE_SQL)
            connection.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self._db_path))

    def append(self, event: dict[str, Any]) -> None:
        columns = ", ".join(EVENT_FIELDS)
        placeholders = ", ".join("?" for _ in EVENT_FIELDS)
        row = [event.get(field, "") for field in EVENT_FIELDS]

        with self._lock:
            with self._connect() as connection:
                connection.execute(
                    f"INSERT INTO events ({columns}, raw_json) VALUES ({placeholders}, ?)",
                    row + [json.dumps(event)],
                )
                connection.commit()

    def all_events(self) -> list[dict[str, Any]]:
        columns = ", ".join(EVENT_FIELDS)
        with self._connect() as connection:
            rows = connection.execute(f"SELECT {columns} FROM events ORDER BY id").fetchall()
        return [dict(zip(EVENT_FIELDS, row)) for row in rows]

    def event_count(self) -> int:
        with self._connect() as connection:
            count = connection.execute("SELECT COUNT(*) FROM events").fetchone()
        return int(count[0]) if count else 0
