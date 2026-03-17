"""Unit tests for event validation logic."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from trustlab.core.events import PARTICIPANT_ID_PATTERN, parse_event_payload


CONDITION_MAP = {
    "A": {"id": "A", "assistant_name": "Astra"},
    "B": {"id": "B", "assistant_name": "System Advisor"},
}


def _valid_payload(**overrides) -> dict:
    payload = {
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
    payload.update(overrides)
    return payload


def _parse(payload: dict):
    return parse_event_payload(
        payload,
        CONDITION_MAP,
        max_latency_ms=300000,
        timestamp_tolerance_seconds=3600,
    )


class TestParticipantIdFormat:
    def test_valid_format_uppercase(self):
        assert PARTICIPANT_ID_PATTERN.match("P-AAAAAAAA")

    def test_valid_format_digits(self):
        assert PARTICIPANT_ID_PATTERN.match("P-12345678")

    def test_valid_format_mixed(self):
        assert PARTICIPANT_ID_PATTERN.match("P-A1B2C3D4")

    def test_reject_lowercase(self):
        assert not PARTICIPANT_ID_PATTERN.match("P-aaaaaaaa")


class TestEventValidation:
    def test_valid_accept(self):
        event = _parse(_valid_payload())
        assert event.decision == "accept"

    def test_decision_case_insensitive(self):
        event = _parse(_valid_payload(decision="ACCEPT"))
        assert event.decision == "accept"

    def test_missing_required_field(self):
        payload = _valid_payload()
        del payload["decision"]
        with pytest.raises(ValueError, match="missing event fields"):
            _parse(payload)

    def test_invalid_participant_id(self):
        with pytest.raises(ValueError, match="participant_id must match"):
            _parse(_valid_payload(participant_id="BADID"))

    def test_unknown_condition_id(self):
        with pytest.raises(ValueError, match="unknown condition_id"):
            _parse(_valid_payload(condition_id="Z"))

    def test_invalid_decision(self):
        with pytest.raises(ValueError, match="decision must be"):
            _parse(_valid_payload(decision="maybe"))

    def test_latency_bounds(self):
        assert _parse(_valid_payload(latency_ms=0)).latency_ms == 0
        with pytest.raises(ValueError, match="latency_ms"):
            _parse(_valid_payload(latency_ms=300001))

    def test_invalid_timestamp_format(self):
        with pytest.raises(ValueError, match="timestamp must be ISO8601"):
            _parse(_valid_payload(timestamp="not-a-date"))

    def test_timestamp_too_old(self):
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        with pytest.raises(ValueError, match="timestamp is"):
            _parse(_valid_payload(timestamp=old_ts))
