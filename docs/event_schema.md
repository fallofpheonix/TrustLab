# TrustLab Event Schema

## Event Type

`decision_event` (one record per completed trial)

## Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `event_id` | string | backend-generated | Unique event identifier. |
| `server_timestamp` | ISO-8601 string | backend-generated | Ingest time at backend. |
| `session_id` | string | yes | Session identifier for one experiment run. |
| `participant_id` | string | yes | Anonymous participant identifier (stable via local storage). |
| `condition` | enum(`A`,`B`) | yes | Deterministic assigned condition. |
| `trial_number` | integer (>=1) | yes | Trial order within session. |
| `scenario_id` | string | yes | Scenario identifier (`s1`..`s6`). |
| `domain` | string | yes | Scenario domain (Medical, Financial, ...). |
| `ai_correct` | boolean | yes | Whether the AI recommendation is ground-truth correct. |
| `is_attention_check` | boolean | yes | Whether this trial is an attention check. |
| `attention_check_passed` | boolean \| null | yes | `true/false` for attention-check trials, `null` otherwise. |
| `ground_truth_action` | enum(`accept`,`override`) | yes | Correct participant action for calibration. |
| `decision` | enum(`accept`,`override`) | yes | Participant decision. |
| `confidence_rating` | integer (1..5) \| null | no | Optional self-reported confidence. |
| `baseline_ai_trust` | integer (1..5) \| null | no | Pre-task trust mini-survey score. |
| `ai_familiarity` | integer (1..5) \| null | no | Pre-task familiarity mini-survey score. |
| `ai_usage_frequency` | enum(`rarely`,`weekly`,`daily`) \| null | no | Pre-task usage-frequency mini-survey response. |
| `timestamp` | ISO-8601 string | yes | Client-side decision timestamp. |
| `latency_ms` | integer (>=0) | yes | Decision latency from trial presentation to submit. |
| `sync_status` | enum(`synced`,`pending`) | client-generated | Backend sync state at time of local export. |

## Invariants

1. Exactly one event per `(session_id, trial_number)`.
2. `ground_truth_action = "accept"` iff `ai_correct = true`, else `"override"` for non-attention trials.
3. `trial_number` increases monotonically for a given `session_id`.
4. `latency_ms` is non-negative.

## Backend API

### `POST /api/log-event`

Request body: one `decision_event` (excluding `event_id`, `server_timestamp`).

Response:

```json
{
  "ok": true,
  "event_id": "uuid",
  "server_timestamp": "2026-03-11T10:20:30.000Z"
}
```

### `GET /api/events.json`

Returns all ingested events.

### `GET /api/events.csv`

Returns all ingested events as CSV.
