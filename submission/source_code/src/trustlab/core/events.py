from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


PARTICIPANT_ID_PATTERN = re.compile(r"^P-[A-Z0-9]{8}$")


@dataclass
class EventRecord:
    participant_id: str
    condition_id: str
    assistant_name: str
    assistant_tone: str
    confidence_frame: str
    decision: str
    decision_matches_recommendation: str
    recommendation_id: str
    recommended_option: str
    timestamp: str
    latency_ms: int
    user_agent: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "participant_id": self.participant_id,
            "condition_id": self.condition_id,
            "assistant_name": self.assistant_name,
            "assistant_tone": self.assistant_tone,
            "confidence_frame": self.confidence_frame,
            "decision": self.decision,
            "decision_matches_recommendation": self.decision_matches_recommendation,
            "recommendation_id": self.recommendation_id,
            "recommended_option": self.recommended_option,
            "timestamp": self.timestamp,
            "latency_ms": self.latency_ms,
            "user_agent": self.user_agent,
        }


def parse_event_payload(
    payload: dict[str, Any],
    condition_map: dict[str, Any],
    *,
    max_latency_ms: int,
    timestamp_tolerance_seconds: int,
) -> EventRecord:
    required_fields = {
        "participant_id",
        "condition_id",
        "assistant_name",
        "assistant_tone",
        "confidence_frame",
        "decision",
        "decision_matches_recommendation",
        "recommendation_id",
        "recommended_option",
        "timestamp",
        "latency_ms",
    }
    missing_fields = sorted(required_fields - set(payload.keys()))
    if missing_fields:
        raise ValueError(f"missing event fields: {missing_fields}")

    participant_id = str(payload["participant_id"]).strip()
    if not PARTICIPANT_ID_PATTERN.fullmatch(participant_id):
        raise ValueError(f"participant_id must match P-[A-Z0-9]{{8}}, got {participant_id!r}")

    condition_id = str(payload["condition_id"]).strip()
    if condition_id not in condition_map:
        raise ValueError(f"unknown condition_id: {condition_id!r}")

    decision = str(payload["decision"]).strip().lower()
    if decision not in {"accept", "reject"}:
        raise ValueError("decision must be 'accept' or 'reject'")

    dmr = str(payload["decision_matches_recommendation"]).strip().lower()

    try:
        latency_ms = int(payload["latency_ms"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"latency_ms must be an integer, got {payload['latency_ms']!r}") from exc
    if latency_ms < 0 or latency_ms > max_latency_ms:
        raise ValueError(f"latency_ms must be in [0, {max_latency_ms}], got {latency_ms}")

    timestamp = str(payload["timestamp"]).strip()
    try:
        observed_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"timestamp must be ISO8601, got {timestamp!r}") from exc

    server_now = datetime.now(timezone.utc)
    skew_seconds = abs((server_now - observed_at.astimezone(timezone.utc)).total_seconds())
    if skew_seconds > timestamp_tolerance_seconds:
        raise ValueError(
            f"timestamp is {skew_seconds:.0f}s from server time (max {timestamp_tolerance_seconds}s)"
        )

    return EventRecord(
        participant_id=participant_id,
        condition_id=condition_id,
        assistant_name=str(payload["assistant_name"]),
        assistant_tone=str(payload["assistant_tone"]),
        confidence_frame=str(payload["confidence_frame"]),
        decision=decision,
        decision_matches_recommendation=dmr,
        recommendation_id=str(payload["recommendation_id"]),
        recommended_option=str(payload["recommended_option"]),
        timestamp=timestamp,
        latency_ms=latency_ms,
        user_agent=str(payload.get("user_agent", "")),
    )
