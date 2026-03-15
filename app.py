from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from trust_server import run_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the task3 trust-calibration prototype.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8003, type=int)
    parser.add_argument("--data-dir", default=str(PROJECT_ROOT / "out"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_server(host=args.host, port=args.port, data_dir=Path(args.data_dir).resolve())


if __name__ == "__main__":
    main()
