from __future__ import annotations

import hashlib
from typing import Any


class AssignmentService:
    """Deterministic server-side condition assignment using SHA256.

    Given a participant_id, the assigned condition is:
        idx = int.from_bytes(SHA256(participant_id)[:4], "big") % n_conditions
    This guarantees even distribution and is reproducible across server restarts.
    """

    def __init__(self, conditions: list[dict[str, Any]]) -> None:
        self._conditions = conditions

    def assign(self, participant_id: str) -> dict[str, Any]:
        """Return the condition deterministically assigned to participant_id."""
        digest = hashlib.sha256(participant_id.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % len(self._conditions)
        return self._conditions[idx]

    def validate(self, participant_id: str, condition_id: str) -> bool:
        """Return True iff condition_id matches the expected server-side assignment."""
        expected = self.assign(participant_id)
        return str(expected["id"]) == str(condition_id)
