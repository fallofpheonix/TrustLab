from __future__ import annotations

import threading
import time
from collections import deque
from typing import Any


class MetricsTracker:
    """Tracks per-request metrics: events/sec, latency stats, condition distribution."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._event_times: deque[float] = deque()
        # Keep only a bounded rolling window of recent latencies to avoid unbounded memory growth.
        self._latencies: deque[float] = deque(maxlen=1000)
        self._condition_counts: dict[str, int] = {}
        self._total_events: int = 0
        self._start_time = time.time()

    def record_event(self, condition_id: str, latency_ms: int) -> None:
        now = time.time()
        with self._lock:
            self._event_times.append(now)
            self._latencies.append(float(latency_ms))
            self._total_events += 1
            self._condition_counts[condition_id] = (
                self._condition_counts.get(condition_id, 0) + 1
            )

    def get_metrics(self) -> dict[str, Any]:
        now = time.time()
        cutoff = now - 60.0
        with self._lock:
            while self._event_times and self._event_times[0] < cutoff:
                self._event_times.popleft()
            eps = len(self._event_times) / 60.0
            total_samples = len(self._latencies)
            if total_samples:
                sorted_lat = sorted(self._latencies)
                mean_lat = sum(sorted_lat) / total_samples
                p50 = sorted_lat[total_samples // 2]
                p95 = sorted_lat[min(int(total_samples * 0.95), total_samples - 1)]
            else:
                mean_lat = p50 = p95 = 0.0
            return {
                "events_per_second": round(eps, 3),
                "total_events": self._total_events,
                "latency_ms": {
                    "mean": round(mean_lat, 1),
                    "p50": round(p50, 1),
                    "p95": round(p95, 1),
                },
                "condition_distribution": dict(self._condition_counts),
                "uptime_seconds": round(now - self._start_time, 1),
            }
