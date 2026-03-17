"""Integration tests for the HTTP API endpoints."""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime, timezone
from http.client import HTTPConnection
from pathlib import Path

import pytest

from trustlab.api.context import AppContext
from trustlab.api.handler import create_request_handler
from trustlab.api.middleware.metrics import RequestMetrics
from trustlab.api.middleware.rate_limit import RequestRateLimiter
from trustlab.services.assignment import ConditionAssignmentService
from trustlab.services.sessions import SessionRegistry
from trustlab.storage.file_event_store import FileEventStore
from http.server import ThreadingHTTPServer


CONDITIONS = [
    {
        "id": "A",
        "assistant_name": "Astra",
        "assistant_tone": "supportive",
        "confidence_frame": "high",
        "headline": "Astra recommends Option A",
        "message": "Test message",
    },
    {
        "id": "B",
        "assistant_name": "System Advisor",
        "assistant_tone": "formal",
        "confidence_frame": "neutral",
        "headline": "System Advisor suggests Option A",
        "message": "Test message",
    },
]


@pytest.fixture(scope="module")
def server(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("data")
    store = FileEventStore(data_dir / "events.jsonl", data_dir / "events.csv")
    assignment_svc = ConditionAssignmentService(CONDITIONS)
    ctx = AppContext(
        web_root=Path(__file__).resolve().parents[2] / "web",
        conditions=CONDITIONS,
        condition_map={str(c["id"]): c for c in CONDITIONS},
        store=store,
        assignment_service=assignment_svc,
        session_registry=SessionRegistry(),
        rate_limiter=RequestRateLimiter(max_requests=1000, window_seconds=60),
        metrics=RequestMetrics(),
        cors_allow_origin="*",
    )
    handler = create_request_handler(ctx)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield port, store, assignment_svc
    httpd.shutdown()


def _get(port: int, path: str) -> tuple[int, dict]:
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request("GET", path)
    resp = conn.getresponse()
    body = json.loads(resp.read())
    return resp.status, body


def _post(port: int, path: str, payload: dict) -> tuple[int, dict]:
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    data = json.dumps(payload).encode()
    conn.request("POST", path, body=data, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    body = json.loads(resp.read())
    return resp.status, body


def _valid_event(participant_id: str, condition_id: str) -> dict:
    return {
        "participant_id": participant_id,
        "condition_id": condition_id,
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


class TestHealthEndpoint:
    def test_health_ok(self, server):
        port, *_ = server
        status, body = _get(port, "/api/health")
        assert status == 200
        assert body["status"] == "ok"


class TestConditionsEndpoint:
    def test_returns_conditions(self, server):
        port, *_ = server
        status, body = _get(port, "/api/conditions")
        assert status == 200
        assert len(body["conditions"]) == 2

    def test_conditions_have_required_fields(self, server):
        port, *_ = server
        _, body = _get(port, "/api/conditions")
        for cond in body["conditions"]:
            for field in ("id", "assistant_name", "assistant_tone", "confidence_frame"):
                assert field in cond


class TestAssignEndpoint:
    def test_assign_returns_condition(self, server):
        port, *_ = server
        status, body = _get(port, "/api/assign?participant_id=P-AAAAAAAA")
        assert status == 200
        assert "condition" in body
        assert body["condition"]["id"] in {"A", "B"}

    def test_assign_missing_param(self, server):
        port, *_ = server
        status, body = _get(port, "/api/assign")
        assert status == 400

    def test_assign_deterministic(self, server):
        port, *_ = server
        _, b1 = _get(port, "/api/assign?participant_id=P-AAAAAAAA")
        _, b2 = _get(port, "/api/assign?participant_id=P-AAAAAAAA")
        assert b1["condition"]["id"] == b2["condition"]["id"]


class TestEventsEndpoint:
    def test_valid_event_accepted(self, server):
        port, _, assignment_svc = server
        pid = "P-AAAAAAAA"
        condition = assignment_svc.resolve(pid)
        status, body = _post(port, "/api/events", _valid_event(pid, condition["id"]))
        assert status == 200
        assert body["status"] == "ok"

    def test_invalid_participant_id(self, server):
        port, _, assignment_svc = server
        event = _valid_event("BADID", "A")
        status, body = _post(port, "/api/events", event)
        assert status == 400

    def test_wrong_condition_assignment(self, server):
        port, _, assignment_svc = server
        pid = "P-AAAAAAAA"
        condition = assignment_svc.resolve(pid)
        wrong_cid = "B" if condition["id"] == "A" else "A"
        status, body = _post(port, "/api/events", _valid_event(pid, wrong_cid))
        assert status == 400
        assert "condition_id" in body["message"].lower() or "assignment" in body["message"].lower()

    def test_missing_field_rejected(self, server):
        port, _, assignment_svc = server
        pid = "P-AAAAAAAA"
        event = _valid_event(pid, assignment_svc.resolve(pid)["id"])
        del event["decision"]
        status, body = _post(port, "/api/events", event)
        assert status == 400

    def test_invalid_decision_rejected(self, server):
        port, _, assignment_svc = server
        pid = "P-AAAAAAAA"
        event = _valid_event(pid, assignment_svc.resolve(pid)["id"])
        event["decision"] = "maybe"
        status, body = _post(port, "/api/events", event)
        assert status == 400

    def test_malformed_json_rejected(self, server):
        port, *_ = server
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request(
            "POST", "/api/events", body=b"not json",
            headers={"Content-Type": "application/json"}
        )
        resp = conn.getresponse()
        assert resp.status == 400

    def test_event_count_increases(self, server):
        port, store, assignment_svc = server
        before = store.event_count()
        pid = "P-BBBBBBBB"
        cid = assignment_svc.resolve(pid)["id"]
        _post(port, "/api/events", _valid_event(pid, cid))
        assert store.event_count() == before + 1


class TestMetricsEndpoint:
    def test_metrics_returns_data(self, server):
        port, *_ = server
        status, body = _get(port, "/api/metrics")
        assert status == 200
        assert "total_events" in body
        assert "latency_ms" in body
        assert "condition_distribution" in body


class TestUnknownEndpoint:
    def test_unknown_post(self, server):
        port, *_ = server
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("POST", "/api/unknown", body=b"{}")
        resp = conn.getresponse()
        assert resp.status == 404
