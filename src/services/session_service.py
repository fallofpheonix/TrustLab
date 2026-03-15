from __future__ import annotations

import threading
from typing import Optional

from models.session import Session


class SessionService:
    """In-memory session manager supporting multi-trial experiment runs."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._lock = threading.Lock()

    def create(self, participant_id: str, condition_id: str) -> Session:
        session = Session.create(participant_id, condition_id)
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> Optional[Session]:
        with self._lock:
            return self._sessions.get(session_id)

    def get_by_participant(self, participant_id: str) -> list[Session]:
        with self._lock:
            return [s for s in self._sessions.values() if s.participant_id == participant_id]

    def complete(self, session_id: str) -> Optional[Session]:
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session.complete()
            return session

    def all_sessions(self) -> list[Session]:
        with self._lock:
            return list(self._sessions.values())

    def session_count(self) -> int:
        with self._lock:
            return len(self._sessions)
