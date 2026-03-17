from __future__ import annotations

import atexit
import csv
import json
import os
import queue
import threading
from pathlib import Path
from typing import Any


EVENT_FIELDS = [
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


class AtomicEventLogger:
    def __init__(self, jsonl_path: Path, csv_path: Path) -> None:
        self._jsonl_path = jsonl_path
        self._csv_path = csv_path
        self._jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

        self._queue: queue.Queue[dict[str, Any] | None] = queue.Queue()
        self._csv_header_written = self._csv_path.exists() and self._csv_path.stat().st_size > 0
        self._worker = threading.Thread(target=self._consume, daemon=True)
        self._worker.start()
        atexit.register(self.close)

    def append(self, event: dict[str, Any]) -> None:
        self._queue.put(event)

    def flush(self) -> None:
        """Block until all queued events have been written to disk."""
        self._queue.join()

    def close(self) -> None:
        if self._worker.is_alive():
            self._queue.put(None)
            self._worker.join(timeout=2)

    def _consume(self) -> None:
        while True:
            event = self._queue.get()
            try:
                if event is None:
                    return
                self._write_event(event)
            finally:
                self._queue.task_done()

    def _write_event(self, event: dict[str, Any]) -> None:
        row = {field: event.get(field, "") for field in EVENT_FIELDS}
        json_line = json.dumps(row, ensure_ascii=True) + "\n"

        with self._lock:
            with self._jsonl_path.open("a", encoding="utf-8") as handle:
                handle.write(json_line)
                handle.flush()
                try:
                    os.fsync(handle.fileno())
                except OSError:
                    pass

            with self._csv_path.open("a", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=EVENT_FIELDS)
                if not self._csv_header_written:
                    writer.writeheader()
                    self._csv_header_written = True
                writer.writerow(row)
                handle.flush()
                try:
                    os.fsync(handle.fileno())
                except OSError:
                    pass

    def all_jsonl_events(self) -> list[dict[str, Any]]:
        # Wait for in-flight writes to land before we read the file.
        self._queue.join()
        if not self._jsonl_path.exists():
            return []

        events: list[dict[str, Any]] = []
        with self._jsonl_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return events
