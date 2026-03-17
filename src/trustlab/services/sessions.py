from __future__ import annotations

import threading

from trustlab.core.session import ParticipantSession


class SessionRegistry:
    def __init__(self) -> None:
        self._sessions: dict[str, ParticipantSession] = {}
        self._lock = threading.Lock()

    def open_session(self, participant_id: str, condition_id: str) -> ParticipantSession:
        session = ParticipantSession.start(participant_id, condition_id)
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> ParticipantSession | None:
        with self._lock:
            return self._sessions.get(session_id)

    def list_for_participant(self, participant_id: str) -> list[ParticipantSession]:
        with self._lock:
            return [session for session in self._sessions.values() if session.participant_id == participant_id]
