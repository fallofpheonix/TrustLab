from __future__ import annotations

from pathlib import Path
from typing import Any

from storage.base import BaseStore
from storage.atomic_logger import AtomicLogger


class FileStore(BaseStore):
    """File-based event store: JSONL as primary storage, CSV as mirror."""

    def __init__(self, jsonl_path: Path, csv_path: Path) -> None:
        self._logger = AtomicLogger(jsonl_path, csv_path)

    def append(self, event: dict[str, Any]) -> None:
        self._logger.append(event)

    def all_events(self) -> list[dict[str, Any]]:
        return self._logger.all_jsonl_events()

    def event_count(self) -> int:
        return self._logger.event_count()
