from __future__ import annotations

import threading
import time
from collections import defaultdict


class RequestRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._requests_by_ip: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def allow(self, client_ip: str) -> bool:
        now = time.monotonic()
        cutoff = now - self._window_seconds

        with self._lock:
            recent = [timestamp for timestamp in self._requests_by_ip[client_ip] if timestamp > cutoff]
            if len(recent) >= self._max_requests:
                self._requests_by_ip[client_ip] = recent
                return False
            recent.append(now)
            self._requests_by_ip[client_ip] = recent
            return True
