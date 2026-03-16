from __future__ import annotations

import csv
import json
import os
import threading
import queue
import atexit
from pathlib import Path
from typing import Any


class AtomicLogger:
    """Thread-safe event logger writing to JSONL (primary) and CSV (mirror).

    Guarantees:
    - Writes happen in a dedicated background worker to prevent blocking HTTP threads.
    - Each JSONL line is written atomically (complete line + fsync).
    - CSV header is written exactly once, tracked in memory to avoid stat() races.
    - All writes are protected by a single mutex.
    - Malformed JSONL lines are skipped gracefully during reads.
    """

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

    def __init__(self, jsonl_path: Path, csv_path: Path) -> None:
        self.jsonl_path = jsonl_path
        self.csv_path = csv_path
        self._lock = threading.Lock()
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        # Track CSV header state in-memory to avoid stat() race conditions.
        self._csv_header_written = (
            self.csv_path.exists() and self.csv_path.stat().st_size > 0
        )
        self._queue: queue.Queue[dict[str, Any] | None] = queue.Queue()
        self._worker = threading.Thread(target=self._process_queue, daemon=True)
        self._worker.start()
        atexit.register(lambda: self._shutdown())

    def _shutdown(self) -> None:
        self._queue.put(None)
        if self._worker.is_alive():
            self._worker.join()

    def append(self, event: dict[str, Any]) -> None:
        """Atomically append one event to the background write queue."""
        self._queue.put(event)

    def _process_queue(self) -> None:
        while True:
            event = self._queue.get()
            if event is None:
                break
            try:
                self._write_event(event)
            finally:
                self._queue.task_done()

    def _write_event(self, event: dict[str, Any]) -> None:
        row = {key: event.get(key, "") for key in self.FIELDNAMES}
        line = json.dumps(row, ensure_ascii=True) + "\n"

        with self._lock:
            # Atomic JSONL append: write a complete line then sync.
            with self.jsonl_path.open("a", encoding="utf-8") as fh:
                fh.write(line)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except OSError:
                    pass

            # CSV append with in-memory header guard.
            with self.csv_path.open("a", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=self.FIELDNAMES)
                if not self._csv_header_written:
                    writer.writeheader()
                    self._csv_header_written = True
                writer.writerow(row)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except OSError:
                    pass

    def all_jsonl_events(self) -> list[dict[str, Any]]:
        """Return all events from JSONL, skipping malformed lines gracefully."""
        if not self.jsonl_path.exists():
            return []
        events: list[dict[str, Any]] = []
        with self.jsonl_path.open("r", encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    events.append(json.loads(raw))
                except json.JSONDecodeError:
                    pass  # Skip corrupted lines without crashing.
        return events

    def event_count(self) -> int:
        return len(self.all_jsonl_events())
