# Validation Proof

Validation date: 2026-03-17

## 1) Automated tests from submission package
Working directory:
- `submission/source_code`

Command:
- `/Users/fallofpheonix/Project/Human AI/TrustLab/.venv/bin/pytest tests/ -q`

Result:
- `51 passed in 0.81s`

## 2) API runtime smoke-test
Command executed from `submission/source_code` with `src/` on path:
- Start server on `127.0.0.1:8011`
- Call `GET /api/health`

Result:
- Status: `200`
- Body: `{"status": "ok"}`

## 3) Analysis script execution
Command:
- `/Users/fallofpheonix/Project/Human AI/TrustLab/.venv/bin/python analysis/analyze_events.py`

Result:
- `rows=151`
- `accept_rate=1.000`
- `mean_latency_ms=100.3`
- `condition_counts: A: 151 (100.0%)`

## 4) Standalone readiness check
A new user can run using only `submission/README.md` by:
1. entering `submission/source_code`
2. creating a virtual environment
3. installing `requirements.txt`
4. running `python app.py --port 8003`

All required dependencies are declared.
