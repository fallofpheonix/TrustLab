from __future__ import annotations

import hashlib
from typing import Any


class ConditionAssignmentService:
    def __init__(self, conditions: list[dict[str, Any]]) -> None:
        if not conditions:
            raise ValueError("conditions list cannot be empty")
        self._conditions = conditions

    def resolve(self, participant_id: str) -> dict[str, Any]:
        digest = hashlib.sha256(participant_id.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % len(self._conditions)
        return self._conditions[index]

    def matches(self, participant_id: str, condition_id: str) -> bool:
        expected = self.resolve(participant_id)
        return str(expected["id"]) == str(condition_id)
