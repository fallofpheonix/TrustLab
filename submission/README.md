# TrustLab Submission Package

## Project overview
TrustLab is a web-based trust-calibration experiment platform for measuring behavioral reliance on AI recommendations. It manipulates cue dimensions (assistant name, tone, confidence framing), captures participant decisions with latency, and exports logs to JSONL/CSV (or SQLite).

This submission satisfies the screening and full-task constraints documented in `doc/submission_guidelines.md`.

## Included deliverables
- `source_code/` — clean runnable backend/frontend code
- `docs/ARCHITECTURE.md` — design and module responsibilities
- `docs/API.md` — endpoint contract documentation
- `docs/USAGE_DEMO.md` — demo flow and operator guide
- `output_samples/` — sample `events.jsonl` and `events.csv`
- `validation/TEST_CASES.md` — critical path test coverage
- `validation/VALIDATION_PROOF.md` — executed validation evidence

## Setup instructions
```bash
cd source_code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run instructions
```bash
cd source_code
source .venv/bin/activate
python app.py --port 8003
```
Open `http://127.0.0.1:8003`.

Optional fixed assignment:
`http://127.0.0.1:8003/?participant_id=P-DEMO0001`

## Dependencies
Runtime dependencies:
- Python 3.11+
- Python standard library

Development dependencies:
- `pytest`
- `ruff`

All dependencies are declared in `source_code/requirements.txt`.
