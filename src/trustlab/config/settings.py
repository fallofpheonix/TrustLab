from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    host: str = os.environ.get("HOST", "127.0.0.1")
    port: int = int(os.environ.get("PORT", "8003"))
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")
    storage_backend: str = os.environ.get("STORAGE_BACKEND", "file")

    rate_limit_max_requests: int = int(os.environ.get("RATE_LIMIT_MAX_REQUESTS", "100"))
    rate_limit_window_seconds: int = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", "60"))

    max_latency_ms: int = int(os.environ.get("MAX_LATENCY_MS", "300000"))
    timestamp_tolerance_seconds: int = int(os.environ.get("TIMESTAMP_TOLERANCE_SECONDS", "3600"))

    cors_allow_origin: str = os.environ.get("CORS_ALLOW_ORIGIN", "*")

    conditions_path: Path = Path(os.environ.get("CONDITIONS_PATH", str(PROJECT_ROOT / "config" / "conditions.json")))
    web_root: Path = Path(os.environ.get("WEB_ROOT", str(PROJECT_ROOT / "web")))
    data_dir: Path = Path(os.environ.get("DATA_DIR", str(PROJECT_ROOT / "data_store")))
