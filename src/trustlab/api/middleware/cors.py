from __future__ import annotations


def build_cors_headers(allow_origin: str) -> dict[str, str]:
    return {
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
