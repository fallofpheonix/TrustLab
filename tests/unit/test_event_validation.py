"""Unit tests for event validation logic."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

import pytest

from models.event import validate_event, PARTICIPANT_ID_RE


CONDITION_MAP = {
    "A": {"id": "A", "assistant_name": "Astra"},
    "B": {"id": "B", "assistant_name": "System Advisor"},
}


def _valid_payload(**overrides) -> dict:
    base = {
        "participant_id": "P-AAAAAAAA",
        "condition_id": "A",
        "assistant_name": "Astra",
        "assistant_tone": "supportive",
        "confidence_frame": "high",
        "decision": "accept",
        "decision_matches_recommendation": "true",
        "recommendation_id": "rec-001",
        "recommended_option": "Option A",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "latency_ms": 1500,
    }
    base.update(overrides)
    return base


class TestParticipantIdFormat:
    def test_valid_format_uppercase(self):
        assert PARTICIPANT_ID_RE.match("P-AAAAAAAA")

    def test_valid_format_digits(self):
        assert PARTICIPANT_ID_RE.match("P-12345678")

    def test_valid_format_mixed(self):
        assert PARTICIPANT_ID_RE.match("P-A1B2C3D4")

    def test_reject_lowercase(self):
        assert not PARTICIPANT_ID_RE.match("P-aaaaaaaa")

    def test_reject_short(self):
        assert not PARTICIPANT_ID_RE.match("P-AAAAAAA")

    def test_reject_long(self):
        assert not PARTICIPANT_ID_RE.match("P-AAAAAAAAA")

    def test_reject_no_prefix(self):
        assert not PARTICIPANT_ID_RE.match("AAAAAAAA")


class TestEventValidation:
    def test_valid_accept(self):
        event = validate_event(_valid_payload(), CONDITION_MAP)
        assert event.decision == "accept"
        assert event.condition_id == "A"

    def test_valid_reject(self):
        event = validate_event(_valid_payload(decision="reject"), CONDITION_MAP)
        assert event.decision == "reject"

    def test_decision_case_insensitive(self):
        event = validate_event(_valid_payload(decision="ACCEPT"), CONDITION_MAP)
        assert event.decision == "accept"

    def test_missing_required_field(self):
        payload = _valid_payload()
        del payload["decision"]
        with pytest.raises(ValueError, match="missing event fields"):
            validate_event(payload, CONDITION_MAP)

    def test_invalid_participant_id(self):
        with pytest.raises(ValueError, match="participant_id must match"):
            validate_event(_valid_payload(participant_id="BADID"), CONDITION_MAP)

    def test_invalid_participant_id_lowercase(self):
        with pytest.raises(ValueError, match="participant_id must match"):
            validate_event(_valid_payload(participant_id="P-aaaaaaaa"), CONDITION_MAP)

    def test_unknown_condition_id(self):
        with pytest.raises(ValueError, match="unknown condition_id"):
            validate_event(_valid_payload(condition_id="Z"), CONDITION_MAP)

    def test_invalid_decision(self):
        with pytest.raises(ValueError, match="decision must be"):
            validate_event(_valid_payload(decision="maybe"), CONDITION_MAP)

    def test_negative_latency(self):
        with pytest.raises(ValueError, match="latency_ms"):
            validate_event(_valid_payload(latency_ms=-1), CONDITION_MAP)

    def test_latency_zero(self):
        event = validate_event(_valid_payload(latency_ms=0), CONDITION_MAP)
        assert event.latency_ms == 0

    def test_latency_at_max(self):
        event = validate_event(
            _valid_payload(latency_ms=300000), CONDITION_MAP, max_latency_ms=300000
        )
        assert event.latency_ms == 300000

    def test_latency_exceeds_max(self):
        with pytest.raises(ValueError, match="latency_ms"):
            validate_event(
                _valid_payload(latency_ms=300001), CONDITION_MAP, max_latency_ms=300000
            )

    def test_invalid_timestamp_format(self):
        with pytest.raises(ValueError, match="timestamp must be ISO8601"):
            validate_event(_valid_payload(timestamp="not-a-date"), CONDITION_MAP)

    def test_timestamp_too_old(self):
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        with pytest.raises(ValueError, match="timestamp is"):
            validate_event(
                _valid_payload(timestamp=old_ts),
                CONDITION_MAP,
                timestamp_tolerance_seconds=3600,
            )

    def test_timestamp_z_suffix(self):
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
        event = validate_event(_valid_payload(timestamp=ts), CONDITION_MAP)
        assert event.timestamp == ts

    def test_user_agent_optional(self):
        payload = _valid_payload()
        payload.pop("user_agent", None)
        event = validate_event(payload, CONDITION_MAP)
        assert event.user_agent == ""

    def test_normalized_output_types(self):
        event = validate_event(_valid_payload(), CONDITION_MAP)
        assert isinstance(event.latency_ms, int)
        assert isinstance(event.participant_id, str)
