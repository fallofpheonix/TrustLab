from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from trustlab.app import run_http_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the task3 trust-calibration prototype.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8003, type=int)
    parser.add_argument("--data-dir", default=str(PROJECT_ROOT / "data_store"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    os.environ["DATA_DIR"] = str(Path(args.data_dir).resolve())
    run_http_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
