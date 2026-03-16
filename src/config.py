from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Config:
    """Central configuration loaded from environment variables with sensible defaults."""

    HOST: str = os.environ.get("HOST", "127.0.0.1")
    PORT: int = int(os.environ.get("PORT", "8003"))
    DATA_DIR: Path = Path(os.environ.get("DATA_DIR", str(PROJECT_ROOT / "data_store")))
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    STORAGE_BACKEND: str = os.environ.get("STORAGE_BACKEND", "file")  # "file" or "sqlite"

    CONDITIONS_PATH: Path = PROJECT_ROOT / "config" / "conditions.json"
    WEB_ROOT: Path = PROJECT_ROOT / "web"

    # Rate limiting
    RATE_LIMIT_MAX_REQUESTS: int = int(os.environ.get("RATE_LIMIT_MAX_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", "60"))

    CORS_ALLOW_ORIGIN: str = os.environ.get("CORS_ALLOW_ORIGIN", "*")
    MAX_LATENCY_MS: int = int(os.environ.get("MAX_LATENCY_MS", "300000"))
    TIMESTAMP_TOLERANCE_SECONDS: int = int(os.environ.get("TIMESTAMP_TOLERANCE_SECONDS", "3600"))
