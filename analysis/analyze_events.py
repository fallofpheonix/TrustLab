from __future__ import annotations

from pathlib import Path
import csv


def main() -> None:
    csv_path = Path(__file__).resolve().parents[1] / "out" / "events.csv"
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    if not rows:
        print("no rows")
        return

    total = len(rows)
    accepts = sum(1 for row in rows if row["decision"] == "accept")
    mean_latency = sum(int(row["latency_ms"]) for row in rows) / total
    print(f"rows={total}")
    print(f"accept_rate={accepts / total:.3f}")
    print(f"mean_latency_ms={mean_latency:.1f}")


if __name__ == "__main__":
    main()
