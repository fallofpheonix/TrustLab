from __future__ import annotations

from http.server import ThreadingHTTPServer

from trustlab.api import AppContext, create_request_handler
from trustlab.api.middleware import RequestMetrics, RequestRateLimiter
from trustlab.config import Settings
from trustlab.services import ConditionAssignmentService, SessionRegistry
from trustlab.storage import FileEventStore, SQLiteEventStore
from trustlab.utils import load_conditions


def run_http_server(host: str | None = None, port: int | None = None) -> None:
    settings = Settings()
    conditions = load_conditions(settings.conditions_path)
    condition_map = {str(condition["id"]): condition for condition in conditions}
    assignment_service = ConditionAssignmentService(conditions)

    settings.data_dir.mkdir(parents=True, exist_ok=True)
    if settings.storage_backend == "sqlite":
        store = SQLiteEventStore(settings.data_dir / "events.db")
    else:
        store = FileEventStore(settings.data_dir / "events.jsonl", settings.data_dir / "events.csv")

    app_context = AppContext(
        web_root=settings.web_root,
        conditions=conditions,
        condition_map=condition_map,
        store=store,
        assignment_service=assignment_service,
        session_registry=SessionRegistry(),
        rate_limiter=RequestRateLimiter(
            max_requests=settings.rate_limit_max_requests,
            window_seconds=settings.rate_limit_window_seconds,
        ),
        metrics=RequestMetrics(),
        cors_allow_origin=settings.cors_allow_origin,
    )

    server_host = host or settings.host
    server_port = port or settings.port
    request_handler = create_request_handler(app_context)
    server = ThreadingHTTPServer((server_host, server_port), request_handler)

    print(f"Serving TrustLab on http://{server_host}:{server_port}")
    print(f"Storage backend: {settings.storage_backend}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
