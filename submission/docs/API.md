# API Documentation

Base URL: `http://127.0.0.1:8003`

## Health
### `GET /api/health`
Response:
```json
{"status": "ok"}
```

## Conditions
### `GET /api/conditions`
Returns all configured experimental conditions.

Response shape:
```json
{
  "conditions": [
    {
      "id": "A",
      "assistant_name": "Astra",
      "assistant_tone": "supportive",
      "confidence_frame": "high",
      "headline": "...",
      "message": "..."
    }
  ]
}
```

## Assignment
### `GET /api/assign?participant_id=P-AAAAAAAA`
Returns deterministic server-side condition assignment.

400 if `participant_id` is missing or malformed.

## Event logging
### `POST /api/events`
Logs one participant event.

Required fields:
- `participant_id`
- `condition_id`
- `assistant_name`
- `assistant_tone`
- `confidence_frame`
- `decision` (`accept` or `reject`)
- `decision_matches_recommendation`
- `recommendation_id`
- `recommended_option`
- `timestamp` (ISO8601)
- `latency_ms`

Server-enriched field:
- `user_agent`

Validation rules:
- participant id format: `P-[A-Z0-9]{8}`
- condition id must exist and match server assignment for that participant
- `latency_ms` in `[0, MAX_LATENCY_MS]`
- timestamp skew within configured tolerance

Success response:
```json
{"status": "ok", "session_id": "<uuid>"}
```

## Metrics
### `GET /api/metrics`
Returns rolling server metrics:
- `events_per_second`
- `total_events`
- `latency_ms.{mean,p50,p95}`
- `condition_distribution`
- `uptime_seconds`
