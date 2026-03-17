# Demo / Usage Guide

## Operator quick-start
1. Start server from `submission/source_code`:
   - `python app.py --port 8003`
2. Open browser:
   - `http://127.0.0.1:8003`
3. Enter or keep generated participant ID.
4. Review AI recommendation and choose `Accept` or `Reject`.
5. Verify event files are updated in `source_code/data_store/`.

## Reproducible assignment demo
Use a fixed participant id in URL:
- `http://127.0.0.1:8003/?participant_id=P-DEMO0001`

Refresh to confirm assignment remains stable.

## Sample operator checks
- `GET /api/health` returns status ok.
- `GET /api/conditions` returns configured cues.
- `GET /api/assign?participant_id=P-AAAAAAAA` returns deterministic condition.
- `POST /api/events` with valid payload returns `status: ok`.

## Analysis demo
Run:
- `python analysis/analyze_events.py`

Output includes:
- total rows
- acceptance rate
- mean latency
- condition distribution
