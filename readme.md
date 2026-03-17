# TrustLab

A lightweight research platform for running trust-calibration A/B experiments. Participants see an AI assistant recommendation under one of several condition variants (name, tone, confidence framing) and decide whether to accept it. All behavioral events and latencies are logged for offline analysis.

## What it does

- Serves a browser-based task from `web/`
- Deterministically assigns each participant to a condition via SHA-256 hash
- Accepts `POST /api/events` payloads, validates them, and persists to JSONL+CSV (or SQLite)
- Exposes `/api/conditions`, `/api/assign`, `/api/health`, and `/api/metrics`
- Per-IP sliding-window rate limiting and basic server metrics out of the box

## Structure

```
src/trustlab/
├── api/          HTTP handler + middleware (CORS, rate-limit, metrics)
├── config/       Environment-driven settings
├── core/         Domain types: EventRecord, ParticipantSession, validation
├── services/     ConditionAssignmentService, SessionRegistry
├── storage/      EventStore ABC + FileEventStore / SQLiteEventStore
└── utils/        condition_loader
```

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit if needed
```

## Run

```bash
python app.py --port 8003
```

Open `http://127.0.0.1:8003`. For a fixed participant (reproducible condition assignment):

```
http://127.0.0.1:8003/?participant_id=P-DEMO0001
```

### Docker

```bash
docker compose up
```

## Tests

```bash
pytest
```

## Key decisions

- **No framework**: stdlib `ThreadingHTTPServer` keeps the dependency list empty at runtime and is sufficient for pilot-scale load.
- **Deterministic assignment**: SHA-256 of `participant_id` gives stable, reproducible condition mapping without a database.
- **Dual-format logging**: JSONL is the primary store (easy to stream); CSV is written in parallel for quick spreadsheet access.
- **SQLite alternative**: set `STORAGE_BACKEND=sqlite` for stronger durability guarantees.
- **Timestamp validation**: server rejects events whose client timestamp drifts more than `TIMESTAMP_TOLERANCE_SECONDS` from server time, catching stale replays.

## Analysis

```bash
python analysis/analyze_events.py
```
