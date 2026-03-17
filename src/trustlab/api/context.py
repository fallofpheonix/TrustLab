from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from trustlab.api.middleware.metrics import RequestMetrics
from trustlab.api.middleware.rate_limit import RequestRateLimiter
from trustlab.services.assignment import ConditionAssignmentService
from trustlab.services.sessions import SessionRegistry
from trustlab.storage.base import EventStore


@dataclass
class AppContext:
    web_root: Path
    conditions: list[dict[str, Any]]
    condition_map: dict[str, dict[str, Any]]
    store: EventStore
    assignment_service: ConditionAssignmentService
    session_registry: SessionRegistry
    rate_limiter: RequestRateLimiter
    metrics: RequestMetrics
    cors_allow_origin: str
