from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class EventStore(ABC):
    @abstractmethod
    def append(self, event: dict[str, Any]) -> None:
        ...

    @abstractmethod
    def all_events(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def event_count(self) -> int:
        ...
