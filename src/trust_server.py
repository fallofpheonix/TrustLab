from __future__ import annotations

import json
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from config import Config
from server.app import AppContext, build_handler
from server.middleware.metrics import MetricsTracker
from server.middleware.rate_limit import RateLimiter
from services.assignment_service import AssignmentService
from services.session_service import SessionService
from storage.file_store import FileStore
from storage.sqlite_store import SQLiteStore


def _load_conditions(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    conditions = payload.get("conditions", [])
    if not isinstance(conditions, list) or not conditions:
        raise RuntimeError(f"invalid condition config: {path}")
    return conditions


def run_server(host: str, port: int, data_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_dir.mkdir(parents=True, exist_ok=True)

    conditions_path = project_root / "config" / "conditions.json"
    conditions = _load_conditions(conditions_path)
    condition_map = {str(c["id"]): c for c in conditions}

    # Select storage backend from environment.
    if Config.STORAGE_BACKEND == "sqlite":
        store: Any = SQLiteStore(data_dir / "events.db")
    else:
        store = FileStore(data_dir / "events.jsonl", data_dir / "events.csv")

    ctx = AppContext(
        web_root=project_root / "web",
        conditions=conditions,
        condition_map=condition_map,
        store=store,
        assignment_service=AssignmentService(conditions),
        session_service=SessionService(),
        rate_limiter=RateLimiter(
            max_requests=Config.RATE_LIMIT_MAX_REQUESTS,
            window_seconds=Config.RATE_LIMIT_WINDOW_SECONDS,
        ),
        metrics=MetricsTracker(),
    )

    handler = build_handler(ctx)
    server = ThreadingHTTPServer((host, port), handler)

    jsonl_path = data_dir / "events.jsonl"
    csv_path = data_dir / "events.csv"
    print(f"Serving task3 prototype on http://{host}:{port}")
    print(f"Logging JSONL to {jsonl_path}")
    print(f"Logging CSV to   {csv_path}")
    print(f"Storage backend: {Config.STORAGE_BACKEND}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
