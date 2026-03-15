from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Condition:
    id: str
    assistant_name: str
    assistant_tone: str
    confidence_frame: str
    headline: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "assistant_name": self.assistant_name,
            "assistant_tone": self.assistant_tone,
            "confidence_frame": self.confidence_frame,
            "headline": self.headline,
            "message": self.message,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Condition":
        return cls(
            id=str(data["id"]),
            assistant_name=str(data["assistant_name"]),
            assistant_tone=str(data["assistant_tone"]),
            confidence_frame=str(data["confidence_frame"]),
            headline=str(data["headline"]),
            message=str(data["message"]),
        )
