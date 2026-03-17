from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def analyze_jsonl(jsonl_path: Path) -> None:
    """Stream-analyze events from JSONL (primary store). Skips malformed lines."""
    if not jsonl_path.exists():
        print("no data file found")
        return

    total = 0
    accepts = 0
    total_latency = 0
    condition_counts: dict[str, int] = defaultdict(int)

    with jsonl_path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue  # Skip malformed lines gracefully.
            total += 1
            if row.get("decision") == "accept":
                accepts += 1
            try:
                total_latency += int(row.get("latency_ms", 0))
            except (TypeError, ValueError):
                pass
            cid = str(row.get("condition_id", "unknown"))
            condition_counts[cid] += 1

    if total == 0:
        print("no rows")
        return

    print(f"rows={total}")
    print(f"accept_rate={accepts / total:.3f}")
    print(f"mean_latency_ms={total_latency / total:.1f}")
    print("condition_counts:")
    for cid, count in sorted(condition_counts.items()):
        print(f"  {cid}: {count} ({count / total:.1%})")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    jsonl_path = project_root / "data_store" / "events.jsonl"
    if not jsonl_path.exists():
        jsonl_path = project_root / "out" / "events.jsonl"
    analyze_jsonl(jsonl_path)


if __name__ == "__main__":
    main()
