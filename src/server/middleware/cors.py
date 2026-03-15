from __future__ import annotations

from config import Config


def get_cors_headers() -> dict[str, str]:
    return {
        "Access-Control-Allow-Origin": Config.CORS_ALLOW_ORIGIN,
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }


# Cached CORS headers (module-level constant for backwards compatibility).
CORS_HEADERS = get_cors_headers()


def apply_cors(send_header_fn: object, headers: dict[str, str] | None = None) -> None:
    """Call send_header for each CORS header via the provided callable."""
    if headers is None:
        headers = get_cors_headers()
    for key, value in headers.items():
        send_header_fn(key, value)  # type: ignore[call-arg]
