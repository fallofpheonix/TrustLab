"""Unit tests for SessionRegistry — critical concurrency and lookup paths."""

from __future__ import annotations

import threading

from trustlab.services.sessions import SessionRegistry


class TestSessionRegistry:
    def test_open_session_returns_session(self):
        registry = SessionRegistry()
        session = registry.open_session("P-AAAAAAAA", "A")
        assert session.participant_id == "P-AAAAAAAA"
        assert session.condition_id == "A"

    def test_get_by_id(self):
        registry = SessionRegistry()
        session = registry.open_session("P-AAAAAAAA", "A")
        fetched = registry.get(session.session_id)
        assert fetched is session

    def test_get_unknown_returns_none(self):
        registry = SessionRegistry()
        assert registry.get("nonexistent-id") is None

    def test_list_for_participant_returns_their_sessions(self):
        registry = SessionRegistry()
        s1 = registry.open_session("P-AAAAAAAA", "A")
        s2 = registry.open_session("P-AAAAAAAA", "B")
        registry.open_session("P-BBBBBBBB", "A")

        results = registry.list_for_participant("P-AAAAAAAA")
        assert len(results) == 2
        ids = {s.session_id for s in results}
        assert s1.session_id in ids and s2.session_id in ids

    def test_concurrent_opens_no_collision(self):
        registry = SessionRegistry()
        sessions = []
        lock = threading.Lock()

        def open_one(i: int) -> None:
            s = registry.open_session(f"P-{i:08X}", "A")
            with lock:
                sessions.append(s)

        threads = [threading.Thread(target=open_one, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(sessions) == 50
        ids = {s.session_id for s in sessions} # pyright: ignore[reportUnknownMemberType]
        assert len(ids) == 50  # all unique
