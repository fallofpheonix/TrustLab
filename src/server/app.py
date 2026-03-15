from __future__ import annotations

import json
from dataclasses import dataclass
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from models.event import validate_event
from services.assignment_service import AssignmentService
from services.session_service import SessionService
from storage.base import BaseStore
from server.middleware.cors import get_cors_headers
from server.middleware.rate_limit import RateLimiter
from server.middleware.metrics import MetricsTracker
from config import Config


@dataclass
class AppContext:
    """Shared application state passed to every request handler."""

    web_root: Path
    conditions: list[dict[str, Any]]
    condition_map: dict[str, dict[str, Any]]
    store: BaseStore
    assignment_service: AssignmentService
    session_service: SessionService
    rate_limiter: RateLimiter
    metrics: MetricsTracker


def build_handler(ctx: AppContext) -> type[SimpleHTTPRequestHandler]:
    """Factory that returns a configured request handler class."""

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(ctx.web_root), **kwargs)

        # ------------------------------------------------------------------ #
        # Suppress default access logging to keep output clean.
        def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
            return

        # ------------------------------------------------------------------ #
        # CORS preflight
        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(HTTPStatus.NO_CONTENT)
            self._add_cors_headers()
            self.send_header("Content-Length", "0")
            self.end_headers()

        # ------------------------------------------------------------------ #
        # GET routing
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path

            if not ctx.rate_limiter.is_allowed(self.client_address[0]):
                self._send_json(
                    {"status": "error", "message": "rate limit exceeded"},
                    status=HTTPStatus.TOO_MANY_REQUESTS,
                )
                return

            if path == "/api/conditions":
                self._send_json({"conditions": ctx.conditions})
                return

            if path == "/api/assign":
                self._handle_assign(parsed.query)
                return

            if path == "/api/health":
                self._send_json({"status": "ok"})
                return

            if path == "/api/metrics":
                self._send_json(ctx.metrics.get_metrics())
                return

            if path == "/admin" or path == "/admin/":
                self.path = "/admin.html"
                super().do_GET()
                return

            if path in {"/", "/index.html"}:
                self.path = "/index.html"
            super().do_GET()

        # ------------------------------------------------------------------ #
        # POST routing
        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/api/events":
                self.send_error(HTTPStatus.NOT_FOUND, "unknown endpoint")
                return

            if not ctx.rate_limiter.is_allowed(self.client_address[0]):
                self._send_json(
                    {"status": "error", "message": "rate limit exceeded"},
                    status=HTTPStatus.TOO_MANY_REQUESTS,
                )
                return

            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                self._send_json(
                    {"status": "error", "message": f"invalid JSON: {exc}"},
                    status=HTTPStatus.BAD_REQUEST,
                )
                return

            payload["user_agent"] = self.headers.get("User-Agent", "")

            # Validate assignment before event validation so callers get a
            # clear error message when condition_id is wrong.
            pid = str(payload.get("participant_id", ""))
            cid = str(payload.get("condition_id", ""))
            if pid and cid and not ctx.assignment_service.validate(pid, cid):
                self._send_json(
                    {
                        "status": "error",
                        "message": (
                            f"condition_id {cid!r} does not match server-side "
                            f"assignment for participant {pid!r}"
                        ),
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )
                return

            try:
                event = validate_event(
                    payload,
                    ctx.condition_map,
                    max_latency_ms=Config.MAX_LATENCY_MS,
                    timestamp_tolerance_seconds=Config.TIMESTAMP_TOLERANCE_SECONDS,
                )
            except ValueError as exc:
                self._send_json(
                    {"status": "error", "message": str(exc)},
                    status=HTTPStatus.BAD_REQUEST,
                )
                return

            ctx.store.append(event.to_dict())
            ctx.metrics.record_event(event.condition_id, event.latency_ms)

            # Update or create session for multi-trial support.
            sessions = ctx.session_service.get_by_participant(event.participant_id)
            active = next(
                (s for s in sessions if s.condition_id == event.condition_id and s.completed_at is None),
                None,
            )
            if active is None:
                active = ctx.session_service.create(event.participant_id, event.condition_id)
            active.add_trial(
                event.recommendation_id,
                event.decision,
                event.latency_ms,
                event.timestamp,
            )

            self._send_json({"status": "ok", "session_id": active.session_id})

        # ------------------------------------------------------------------ #
        # Helpers

        def _handle_assign(self, query_string: str) -> None:
            params = parse_qs(query_string)
            pid_list = params.get("participant_id", [])
            if not pid_list:
                self._send_json(
                    {"status": "error", "message": "participant_id query param required"},
                    status=HTTPStatus.BAD_REQUEST,
                )
                return
            participant_id = pid_list[0]
            condition = ctx.assignment_service.assign(participant_id)
            self._send_json(
                {"participant_id": participant_id, "condition": condition}
            )

        def _add_cors_headers(self) -> None:
            for key, value in get_cors_headers().items():
                self.send_header(key, value)

        def _send_json(
            self,
            payload: dict[str, Any],
            status: HTTPStatus = HTTPStatus.OK,
        ) -> None:
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self._add_cors_headers()
            self.end_headers()
            self.wfile.write(encoded)

    return Handler
