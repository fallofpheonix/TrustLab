# Task 3 Overview

## Assignment

Task 3 is a trust-calibration experimentation platform. The screening task is a minimal web prototype with A/B cue variation, a single recommendation acceptance decision, and JSON/CSV logging of participant behavior and latency.

## Current Repository State

- Proposal, problem statement, roadmap, and submission-guideline docs exist.
- A runnable local prototype now exists in `task3/app.py`.
- File-backed logging exists in `task3/src/trust_server.py`.
- Condition configuration exists in `task3/config/conditions.json`.
- Static frontend assets exist in `task3/web/`.
- Sample outputs exist in `task3/out/events.jsonl` and `task3/out/events.csv`.
- A lightweight analysis helper exists in `task3/analysis/analyze_events.py`.

## Current Implementation

- Deterministic participant assignment:
  participant IDs are generated locally and persisted in `localStorage`, or can be injected with `?participant_id=...`.
- Deterministic condition assignment:
  the client hashes `participant_id` and maps it onto `task3/config/conditions.json`.
- Logging schema:
  `participant_id`, `condition_id`, `assistant_name`, `assistant_tone`, `confidence_frame`, `decision`, `decision_matches_recommendation`, `recommendation_id`, `recommended_option`, `timestamp`, `latency_ms`, `user_agent`.
- Backend:
  Python standard-library HTTP server with `/api/conditions` and `/api/events`.
- Persistence:
  append-only `events.jsonl` plus synchronized `events.csv`.

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` is intentionally empty of third-party runtime dependencies; the prototype uses Python standard library only.

## Run

```bash
python app.py --port 8003
```

Then open:

```text
http://127.0.0.1:8003
```

Optional fixed participant for reproducible A/B assignment:

```text
http://127.0.0.1:8003/?participant_id=P-DEMO001
```

## Outputs

- Log files:
  `task3/out/events.jsonl`
  `task3/out/events.csv`
- Analysis helper:

```bash
python analysis/analyze_events.py
```

## Recommended Next Build Step

- Add a richer multi-trial task instead of a single recommendation.
- Move cue config to researcher-editable task definitions.
- Replace the standard-library server with a framework-backed app only if experiment scope expands.
