from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class Trial:
    trial_number: int
    recommendation_id: str
    decision: str
    latency_ms: int
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "trial_number": self.trial_number,
            "recommendation_id": self.recommendation_id,
            "decision": self.decision,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
        }


@dataclass
class Session:
    session_id: str
    participant_id: str
    condition_id: str
    trials: list[Trial] = field(default_factory=list)
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: Optional[str] = None

    @classmethod
    def create(cls, participant_id: str, condition_id: str) -> "Session":
        return cls(
            session_id=str(uuid.uuid4()),
            participant_id=participant_id,
            condition_id=condition_id,
        )

    def add_trial(
        self,
        recommendation_id: str,
        decision: str,
        latency_ms: int,
        timestamp: str,
    ) -> Trial:
        trial = Trial(
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "participant_id": self.participant_id,
            "condition_id": self.condition_id,
            "trials": [t.to_dict() for t in self.trials],
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
