"""Integration tests for concurrent event logging."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from storage.atomic_logger import AtomicLogger
from storage.file_store import FileStore


class TestConcurrentFileStore:
    def test_no_data_loss_under_concurrency(self, tmp_path: Path):
        store = FileStore(tmp_path / "events.jsonl", tmp_path / "events.csv")
        n_threads = 10
        n_events = 50

        def worker(tid: int) -> None:
            for i in range(n_events):
                store.append(
                    {
                        "participant_id": f"P-{tid:04X}{i:04X}",
                        "condition_id": "A" if i % 2 == 0 else "B",
                        "decision": "accept",
                        "latency_ms": tid * 10 + i,
                    }
                )

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        events = store.all_events()
        assert len(events) == n_threads * n_events

    def test_jsonl_lines_are_valid(self, tmp_path: Path):
        store = FileStore(tmp_path / "events.jsonl", tmp_path / "events.csv")
        n = 100
        for i in range(n):
            store.append({"participant_id": f"P-{i:08X}", "decision": "reject"})

        jsonl_path = tmp_path / "events.jsonl"
        lines = jsonl_path.read_text().strip().split("\n")
        assert len(lines) == n
        for line in lines:
            obj = json.loads(line)  # Must not raise.
            assert "participant_id" in obj

    def test_csv_has_single_header_under_concurrency(self, tmp_path: Path):
        store = FileStore(tmp_path / "events.jsonl", tmp_path / "events.csv")
        n_threads = 5

        def worker(tid: int) -> None:
            for i in range(20):
                store.append({"participant_id": f"P-{tid:04X}{i:04X}", "decision": "accept"})

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        csv_content = (tmp_path / "events.csv").read_text()
        assert csv_content.count("participant_id") == 1

    def test_event_count_matches_append_calls(self, tmp_path: Path):
        store = FileStore(tmp_path / "events.jsonl", tmp_path / "events.csv")
        n = 42
        for i in range(n):
            store.append({"participant_id": f"P-{i:08X}", "decision": "accept"})
        assert store.event_count() == n
