from __future__ import annotations

import threading
import time
from collections import deque
from typing import Any


class RequestMetrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._event_times = deque()
        self._latency_samples = deque(maxlen=1000)
        self._condition_counts: dict[str, int] = {}
        self._total_events = 0
        self._started_at = time.time()

    def record_event(self, condition_id: str, latency_ms: int) -> None:
        now = time.time()
        with self._lock:
            self._event_times.append(now)
            self._latency_samples.append(float(latency_ms))
            self._total_events += 1
            self._condition_counts[condition_id] = self._condition_counts.get(condition_id, 0) + 1

    def snapshot(self) -> dict[str, Any]:
        now = time.time()
        with self._lock:
            self._trim_event_window(now)
            samples = sorted(self._latency_samples)
            sample_count = len(samples)
            if sample_count:
                mean = sum(samples) / sample_count
                p50 = samples[sample_count // 2]
                # TODO: use t-digest when metrics scale beyond local experiment usage.
                p95 = samples[min(int(sample_count * 0.95), sample_count - 1)]
            else:
                mean = p50 = p95 = 0.0

            return {
                "events_per_second": round(len(self._event_times) / 60.0, 3),
                "total_events": self._total_events,
                "latency_ms": {"mean": round(mean, 1), "p50": round(p50, 1), "p95": round(p95, 1)},
                "condition_distribution": dict(self._condition_counts),
                "uptime_seconds": round(now - self._started_at, 1),
            }

    def _trim_event_window(self, now: float) -> None:
        cutoff = now - 60.0
        while self._event_times and self._event_times[0] < cutoff:
            self._event_times.popleft()
