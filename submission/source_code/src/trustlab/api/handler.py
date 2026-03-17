from __future__ import annotations

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler
from typing import Any
from urllib.parse import parse_qs, urlparse

from trustlab.api.context import AppContext
from trustlab.api.middleware.cors import build_cors_headers
from trustlab.core import PARTICIPANT_ID_PATTERN, parse_event_payload


def create_request_handler(context: AppContext) -> type[SimpleHTTPRequestHandler]:
    class RequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(context.web_root), **kwargs)

        def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
            return

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(HTTPStatus.NO_CONTENT)
            self._send_cors_headers()
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path

            if not self._within_rate_limit():
                return

            if path == "/api/health":
                self._send_json({"status": "ok"})
                return

            if path == "/api/conditions":
                self._send_json({"conditions": context.conditions})
                return

            if path == "/api/assign":
                self._handle_assignment(parsed.query)
                return

            if path == "/api/metrics":
                self._send_json(context.metrics.snapshot())
                return

            if path in {"/admin", "/admin/"}:
                self.path = "/admin.html"
                super().do_GET()
                return

            if path in {"/", "/index.html"}:
                self.path = "/index.html"
            super().do_GET()

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/api/events":
                self.send_error(HTTPStatus.NOT_FOUND, "unknown endpoint")
                return

            if not self._within_rate_limit():
                return

            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                self._send_json(
                    {"status": "error", "message": f"invalid JSON: {exc}"},
                    status=HTTPStatus.BAD_REQUEST,
                )
                return

            payload["user_agent"] = self.headers.get("User-Agent", "")

            participant_id = str(payload.get("participant_id", "")).strip()
            condition_id = str(payload.get("condition_id", "")).strip()
            if participant_id and condition_id and not context.assignment_service.matches(participant_id, condition_id):
                self._send_json(
                    {
                        "status": "error",
                        "message": f"condition_id {condition_id!r} does not match server-side assignment for participant {participant_id!r}",
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )
                return

            try:
                event = parse_event_payload(
                    payload,
                    context.condition_map,
                    max_latency_ms=300000,
                    timestamp_tolerance_seconds=3600,
                )
            except ValueError as exc:
                self._send_json({"status": "error", "message": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return

            try:
                context.store.append(event.as_dict())
                context.metrics.record_event(event.condition_id, event.latency_ms)
                session = self._resolve_session(event.participant_id, event.condition_id)
                session.append_trial(event.recommendation_id, event.decision, event.latency_ms, event.timestamp)
                self._send_json({"status": "ok", "session_id": session.session_id})
            except Exception as exc:
                self._send_json(
                    {"status": "error", "message": f"internal server error: {exc}"},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

        def _within_rate_limit(self) -> bool:
            if context.rate_limiter.allow(self.client_address[0]):
                return True
            self._send_json(
                {"status": "error", "message": "rate limit exceeded"},
                status=HTTPStatus.TOO_MANY_REQUESTS,
            )
            return False

        def _handle_assignment(self, query_string: str) -> None:
            participant_ids = parse_qs(query_string).get("participant_id", [])
            if not participant_ids:
                self._send_json(
                    {"status": "error", "message": "participant_id query param required"},
                    status=HTTPStatus.BAD_REQUEST,
                )
                return

            participant_id = participant_ids[0].strip()
            if not PARTICIPANT_ID_PATTERN.fullmatch(participant_id):
                self._send_json(
                    {"status": "error", "message": "invalid participant_id format"},
                    status=HTTPStatus.BAD_REQUEST,
                )
                return

            condition = context.assignment_service.resolve(participant_id)
            self._send_json({"participant_id": participant_id, "condition": condition})

        def _resolve_session(self, participant_id: str, condition_id: str):
            sessions = context.session_registry.list_for_participant(participant_id)
            for active_session in sessions:
                if active_session.condition_id == condition_id and active_session.completed_at is None:
                    return active_session
            return context.session_registry.open_session(participant_id, condition_id)

        def _send_cors_headers(self) -> None:
            for key, value in build_cors_headers(context.cors_allow_origin).items():
                self.send_header(key, value)

        def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(encoded)

    return RequestHandler
