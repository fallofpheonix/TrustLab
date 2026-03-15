from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseStore(ABC):
    """Abstract base class for event storage backends."""

    @abstractmethod
    def append(self, event: dict[str, Any]) -> None:
        """Append an event to the store. Must be thread-safe."""
        ...

    @abstractmethod
    def all_events(self) -> list[dict[str, Any]]:
        """Return all stored events."""
        ...

    @abstractmethod
    def event_count(self) -> int:
        """Return total number of stored events."""
        ...
