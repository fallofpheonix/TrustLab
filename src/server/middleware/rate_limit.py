from __future__ import annotations

import threading
import time
from collections import defaultdict


class RateLimiter:
    """Sliding-window per-IP rate limiter."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, client_ip: str) -> bool:
        """Return True if the request is within the allowed rate."""
        now = time.monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            timestamps = self._requests[client_ip]
            self._requests[client_ip] = [t for t in timestamps if t > cutoff]
            if len(self._requests[client_ip]) >= self.max_requests:
                return False
            self._requests[client_ip].append(now)
            return True
