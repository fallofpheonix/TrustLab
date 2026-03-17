"""Unit tests for deterministic condition assignment."""

from __future__ import annotations

import hashlib

import pytest

from trustlab.services.assignment import ConditionAssignmentService


CONDITIONS = [
    {"id": "A", "assistant_name": "Astra"},
    {"id": "B", "assistant_name": "System Advisor"},
]


@pytest.fixture
def service():
    return ConditionAssignmentService(CONDITIONS)


class TestAssignmentService:
    def test_returns_a_condition(self, service):
        condition = service.resolve("P-AAAAAAAA")
        assert condition["id"] in {"A", "B"}

    def test_deterministic(self, service):
        c1 = service.resolve("P-AAAAAAAA")
        c2 = service.resolve("P-AAAAAAAA")
        assert c1["id"] == c2["id"]

    def test_sha256_matches_manual(self, service):
        pid = "P-TESTAAAA"
        digest = hashlib.sha256(pid.encode("utf-8")).digest()
        expected_idx = int.from_bytes(digest[:4], "big") % len(CONDITIONS)
        expected_id = CONDITIONS[expected_idx]["id"]
        assert service.resolve(pid)["id"] == expected_id

    def test_validate_correct(self, service):
        pid = "P-AAAAAAAA"
        condition = service.resolve(pid)
        assert service.matches(pid, condition["id"]) is True

    def test_validate_incorrect(self, service):
        pid = "P-AAAAAAAA"
        condition = service.resolve(pid)
        wrong_id = "B" if condition["id"] == "A" else "A"
        assert service.matches(pid, wrong_id) is False

    def test_distribution_roughly_even(self, service):
        """With 1000 random-looking IDs the split should be near 50/50."""
        counts: dict[str, int] = {"A": 0, "B": 0}
        for i in range(1000):
            pid = f"P-{i:08X}"
            cid = service.resolve(pid)["id"]
            counts[cid] += 1
        # Neither bucket should be overwhelmingly dominant (allow ±20%)
        assert abs(counts["A"] - counts["B"]) < 200

    def test_all_participants_get_valid_condition(self, service):
        ids = [f"P-{i:08X}" for i in range(100)]
        for pid in ids:
            c = service.resolve(pid)
            assert c["id"] in {"A", "B"}
