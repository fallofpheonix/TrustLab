from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
import csv
import json
import threading


@dataclass
class AppConfig:
    project_root: Path
    web_root: Path
    data_dir: Path
    jsonl_path: Path
    csv_path: Path
    conditions_path: Path


class EventLogger:
    fieldnames = [
        "participant_id",
        "condition_id",
        "assistant_name",
        "assistant_tone",
        "confidence_frame",
        "decision",
        "decision_matches_recommendation",
        "recommendation_id",
        "recommended_option",
        "timestamp",
        "latency_ms",
        "user_agent",
    ]

    def __init__(self, jsonl_path: Path, csv_path: Path) -> None:
        self.jsonl_path = jsonl_path
        self.csv_path = csv_path
        self._lock = threading.Lock()
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: dict[str, Any]) -> None:
        row = {key: event.get(key, "") for key in self.fieldnames}
        with self._lock:
            with self.jsonl_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=True) + "\n")

            write_header = not self.csv_path.exists() or self.csv_path.stat().st_size == 0
            with self.csv_path.open("a", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=self.fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerow(row)


def _load_conditions(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    conditions = payload.get("conditions", [])
    if not isinstance(conditions, list) or not conditions:
        raise RuntimeError(f"invalid condition config: {path}")
    return conditions


def _validate_event(payload: dict[str, Any], conditions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    required = {
        "participant_id",
        "condition_id",
        "assistant_name",
        "assistant_tone",
        "confidence_frame",
        "decision",
        "decision_matches_recommendation",
        "recommendation_id",
        "recommended_option",
        "timestamp",
        "latency_ms",
    }
    missing = sorted(key for key in required if key not in payload)
    if missing:
        raise ValueError(f"missing event fields: {missing}")

    condition_id = str(payload["condition_id"])
    if condition_id not in conditions:
        raise ValueError(f"unknown condition_id: {condition_id}")

    decision = str(payload["decision"]).lower()
    if decision not in {"accept", "reject"}:
        raise ValueError("decision must be accept or reject")

    latency_ms = int(payload["latency_ms"])
    if latency_ms < 0:
        raise ValueError("latency_ms must be non-negative")

    normalized = {
        "participant_id": str(payload["participant_id"]),
        "condition_id": condition_id,
        "assistant_name": str(payload["assistant_name"]),
        "assistant_tone": str(payload["assistant_tone"]),
        "confidence_frame": str(payload["confidence_frame"]),
        "decision": decision,
        "decision_matches_recommendation": str(payload["decision_matches_recommendation"]).lower(),
        "recommendation_id": str(payload["recommendation_id"]),
        "recommended_option": str(payload["recommended_option"]),
        "timestamp": str(payload["timestamp"]),
        "latency_ms": latency_ms,
        "user_agent": str(payload.get("user_agent", "")),
    }
    return normalized


def build_handler(config: AppConfig, logger: EventLogger, conditions: list[dict[str, Any]]) -> type[SimpleHTTPRequestHandler]:
    condition_map = {str(item["id"]): item for item in conditions}

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(config.web_root), **kwargs)

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/api/conditions":
                self._send_json({"conditions": conditions})
                return
            if self.path in {"/", "/index.html"}:
                self.path = "/index.html"
            super().do_GET()

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/api/events":
                self.send_error(HTTPStatus.NOT_FOUND, "unknown endpoint")
                return

            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
                payload["user_agent"] = self.headers.get("User-Agent", "")
                event = _validate_event(payload, condition_map)
                logger.append(event)
            except Exception as exc:
                self._send_json({"status": "error", "message": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return

            self._send_json({"status": "ok"})

        def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    return Handler


def run_server(host: str, port: int, data_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    config = AppConfig(
        project_root=project_root,
        web_root=project_root / "web",
        data_dir=data_dir,
        jsonl_path=data_dir / "events.jsonl",
        csv_path=data_dir / "events.csv",
        conditions_path=project_root / "config" / "conditions.json",
    )
    config.data_dir.mkdir(parents=True, exist_ok=True)
    conditions = _load_conditions(config.conditions_path)
    logger = EventLogger(config.jsonl_path, config.csv_path)
    handler = build_handler(config, logger, conditions)
    server = ThreadingHTTPServer((host, port), handler)

    print(f"Serving task3 prototype on http://{host}:{port}")
    print(f"Logging JSONL to {config.jsonl_path}")
    print(f"Logging CSV to   {config.csv_path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
