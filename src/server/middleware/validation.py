from __future__ import annotations

from models.event import validate_event, Event
from typing import Any


def validate_request_event(
    payload: dict[str, Any],
    condition_map: dict[str, Any],
    max_latency_ms: int = 300000,
    timestamp_tolerance_seconds: int = 3600,
) -> Event:
    """Thin wrapper around validate_event for use as request middleware."""
    return validate_event(
        payload,
        condition_map,
        max_latency_ms=max_latency_ms,
        timestamp_tolerance_seconds=timestamp_tolerance_seconds,
    )
