from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TrialRecord:
    trial_number: int
    recommendation_id: str
    decision: str
    latency_ms: int
    timestamp: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "trial_number": self.trial_number,
            "recommendation_id": self.recommendation_id,
            "decision": self.decision,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
        }


@dataclass
class ParticipantSession:
    session_id: str
    participant_id: str
    condition_id: str
    trials: list[TrialRecord] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None

    @classmethod
    def start(cls, participant_id: str, condition_id: str) -> "ParticipantSession":
        return cls(
            session_id=str(uuid.uuid4()),
            participant_id=participant_id,
            condition_id=condition_id,
        )

    def append_trial(self, recommendation_id: str, decision: str, latency_ms: int, timestamp: str) -> TrialRecord:
        trial = TrialRecord(
            trial_number=len(self.trials) + 1,
            recommendation_id=recommendation_id,
            decision=decision,
            latency_ms=latency_ms,
            timestamp=timestamp,
        )
        self.trials.append(trial)
        return trial

    def complete(self) -> None:
        self.completed_at = datetime.now(timezone.utc).isoformat()
