# TrustLab: Humanlike AI Systems and Trust Attribution

Modular experiment platform for trust-calibration studies in AI-assisted decision tasks.

## Scope

- Two-condition cue manipulation (`A`/`B`).
- Recommendation acceptance task (`accept` vs `override`).
- High-resolution behavioral logging with latency.
- Export pipeline (`JSON` and `CSV`).
- Analysis notebook for condition-level behavioral metrics.

## Screening Test Compliance

| Requirement | Status | Evidence |
| --- | --- | --- |
| Simple web page with two conditions (A/B) differing in cue | Implemented | `TrustLabPlatform.jsx` (`CONDITIONS`, deterministic assignment) |
| One decision task (accept/reject AI recommendation) | Implemented | `TrustLabPlatform.jsx` (`Accept` / `Override` flow) |
| Logging includes `participant_id`, `condition`, `decision`, `timestamp`, `latency_ms` | Implemented | `TrustLabPlatform.jsx`, `backend/lib/event-core.js` |
| JSON/CSV export | Implemented | `GET /api/events.json`, `GET /api/events.csv` |
| README with condition logic, logging, local run, sample output | Implemented | This file |
| Sample output file | Implemented | `test_results/sample_output.csv` |

## Condition Logic

- Stable participant identity is stored in browser local storage (`trustlab.participant_id`).
- Condition assignment is deterministic from participant hash:

```text
condition = hash(participant_id) % 2 == 0 ? "A" : "B"
```

- This avoids reassignment on refresh and supports reproducibility.

### Condition Cues

- **A**: neutral/technical framing.
- **B**: humanlike/conversational framing.

(Implemented via condition configuration in `TrustLabPlatform.jsx`.)

## Decision Task

- Participant receives AI recommendation per scenario.
- Participant chooses:
  - `accept`
  - `override`
- Decision latency is measured from scenario render to response submit.
- Includes baseline trust mini-survey and one attention-check scenario.

## Logging Implementation

### Client side

Per completed trial, frontend emits one event to `POST /api/log-event`.

Required screening fields in each event:

- `participant_id`
- `condition`
- `decision`
- `timestamp`
- `latency_ms`

### Backend

Validation and persistence pipeline:

1. `POST /api/log-event` validates event payload.
2. Backend enriches with:
   - `event_id`
   - `server_timestamp`
   - `quality_score` / `quality_flags`
3. Event is appended to local store (`backend/data/events.jsonl`).

Export/report endpoints:

- `GET /api/health`
- `GET /api/events.json`
- `GET /api/events.csv`
- `GET /api/quality-report.json`

## Event Schema

Full schema reference:

- `docs/event_schema.md`

Core required fields are enforced by backend validators in `backend/lib/event-core.js`.

## Run Locally

### Prerequisites

- Node.js 18+
- npm

### 1) Install

```bash
npm install
```

### 2) Start backend (terminal 1)

```bash
npm run dev:backend
```

### 3) Start frontend (terminal 2)

```bash
npm run dev
```

### 4) Open app

- Frontend: `http://127.0.0.1:5173/`
- Backend health: `http://127.0.0.1:8787/api/health`

### Build check

```bash
npm run build
npm run preview
```

### Automated verification

```bash
npm run test
npm run verify
```

## Sample Output Files

- Screening sample: `test_results/sample_output.csv`
- Additional sample: `sample_output.csv`
- Runtime local store: `backend/data/events.jsonl`
- Verification logs:
  - `test_results/verify_output.txt`
  - `test_results/build_output.txt`
  - `test_results/live_check_response_body.txt`

## Analysis Notebook

- Notebook: `analysis/analysis.ipynb`
- Dependency file: `analysis/requirements.txt`

Install analysis deps:

```bash
python3 -m pip install -r analysis/requirements.txt
```

Notebook computes condition-level:

- reliance rate
- override rate
- mean latency

## Deployment

- Frontend (Vercel): [https://trustlab-fallofpheonix.vercel.app](https://trustlab-fallofpheonix.vercel.app)
- Backend persistence endpoints are configured for local runtime in this repo.

## Repository Layout

```text
TrustLab/
├── TrustLabPlatform.jsx
├── src/main.jsx
├── backend/
│   ├── server.js
│   ├── app.js
│   └── lib/
├── api/
├── docs/event_schema.md
├── analysis/analysis.ipynb
├── test_results/sample_output.csv
└── README.md
```

## Submission Checklist

For submission email to `human-ai@cern.ch`:

- CV/resume (attachment)
- GitHub repo link
- Test results (`test_results/`)
- README (this file)
- Sample output file (`test_results/sample_output.csv`)

## Notes

- Current backend is local-first file persistence.
- Public deployment of backend API is optional for screening and required only for full production operation.
