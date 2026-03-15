"""Unit tests for AtomicLogger — thread-safety and data integrity."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from storage.atomic_logger import AtomicLogger


@pytest.fixture
def tmp_paths(tmp_path: Path):
    return tmp_path / "events.jsonl", tmp_path / "events.csv"


class TestAtomicLogger:
    def test_append_creates_files(self, tmp_paths):
        jsonl, csv = tmp_paths
        logger = AtomicLogger(jsonl, csv)
        logger.append({"participant_id": "P-AAAAAAAA", "decision": "accept", "latency_ms": 100})
        assert jsonl.exists()
        assert csv.exists()

    def test_jsonl_line_is_valid_json(self, tmp_paths):
        jsonl, csv = tmp_paths
        logger = AtomicLogger(jsonl, csv)
        logger.append({"participant_id": "P-AAAAAAAA", "decision": "accept", "latency_ms": 100})
        lines = jsonl.read_text().strip().split("\n")
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["participant_id"] == "P-AAAAAAAA"

    def test_csv_header_written_once(self, tmp_paths):
        jsonl, csv = tmp_paths
        logger = AtomicLogger(jsonl, csv)
        for _ in range(3):
            logger.append({"participant_id": "P-AAAAAAAA", "decision": "accept"})
        content = csv.read_text()
        assert content.count("participant_id") == 1

    def test_multiple_appends(self, tmp_paths):
        jsonl, csv = tmp_paths
        logger = AtomicLogger(jsonl, csv)
        for i in range(5):
            logger.append({"participant_id": f"P-{i:08X}", "decision": "accept"})
        events = logger.all_jsonl_events()
        assert len(events) == 5

    def test_concurrent_appends_produce_no_corruption(self, tmp_paths):
        jsonl, csv = tmp_paths
        logger = AtomicLogger(jsonl, csv)
        n_threads = 20
        n_per_thread = 10

        def worker(tid: int) -> None:
            for i in range(n_per_thread):
                logger.append({"participant_id": f"P-{tid:04X}{i:04X}", "decision": "accept"})

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        events = logger.all_jsonl_events()
        assert len(events) == n_threads * n_per_thread

    def test_malformed_jsonl_lines_skipped(self, tmp_paths):
        jsonl, csv = tmp_paths
        logger = AtomicLogger(jsonl, csv)
        logger.append({"participant_id": "P-AAAAAAAA", "decision": "accept"})
        # Inject a malformed line directly.
        with jsonl.open("a") as fh:
            fh.write("NOT VALID JSON\n")
        logger.append({"participant_id": "P-BBBBBBBB", "decision": "reject"})
        events = logger.all_jsonl_events()
        # 2 valid lines; the malformed one is silently skipped.
        assert len(events) == 2

    def test_csv_header_not_duplicated_on_reopen(self, tmp_paths):
        jsonl, csv = tmp_paths
        logger = AtomicLogger(jsonl, csv)
        logger.append({"participant_id": "P-AAAAAAAA", "decision": "accept"})
        # Simulate reopening (e.g. server restart) — header already exists.
        logger2 = AtomicLogger(jsonl, csv)
        logger2.append({"participant_id": "P-BBBBBBBB", "decision": "reject"})
        content = csv.read_text()
        assert content.count("participant_id") == 1
