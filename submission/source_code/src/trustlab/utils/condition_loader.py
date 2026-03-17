from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_conditions(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise RuntimeError(f"condition config not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    conditions = data.get("conditions")
    if not isinstance(conditions, list) or not conditions:
        raise RuntimeError(f"invalid condition payload in {path}")

    for idx, condition in enumerate(conditions):
        if "id" not in condition:
            raise RuntimeError(f"condition #{idx + 1} is missing id")

    return conditions
