from __future__ import annotations

from pathlib import Path
from typing import Any

from trustlab.storage.atomic_event_logger import AtomicEventLogger
from trustlab.storage.base import EventStore


class FileEventStore(EventStore):
    def __init__(self, jsonl_path: Path, csv_path: Path) -> None:
        self._logger = AtomicEventLogger(jsonl_path, csv_path)

    def append(self, event: dict[str, Any]) -> None:
        self._logger.append(event)

    def flush(self) -> None:
        self._logger.flush()

    def all_events(self) -> list[dict[str, Any]]:
        return self._logger.all_jsonl_events()

    def event_count(self) -> int:
        return len(self._logger.all_jsonl_events())
