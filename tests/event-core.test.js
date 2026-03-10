import assert from "node:assert/strict";
import test from "node:test";
import { qualityForEvent, summarizeSessions, toCsv, validateEvent } from "../backend/lib/event-core.js";

function baseEvent(overrides = {}) {
  return {
    session_id: "s-1",
    participant_id: "p-1",
    condition: "A",
    trial_number: 1,
    scenario_id: "sc-1",
    domain: "medical",
    ai_correct: true,
    is_attention_check: false,
    attention_check_passed: null,
    ground_truth_action: "accept",
    decision: "accept",
    timestamp: "2026-03-11T10:00:00.000Z",
    latency_ms: 1200,
    total_expected_trials: 6,
    ...overrides,
  };
}

test("validateEvent accepts valid event", () => {
  const err = validateEvent(baseEvent());
  assert.equal(err, null);
});

test("validateEvent rejects missing required field", () => {
  const e = baseEvent();
  delete e.session_id;
  const err = validateEvent(e);
  assert.equal(err, "missing field: session_id");
});

test("validateEvent rejects malformed values", () => {
  assert.equal(validateEvent(baseEvent({ condition: "Z" })), "invalid condition");
  assert.equal(validateEvent(baseEvent({ decision: "maybe" })), "invalid decision");
  assert.equal(validateEvent(baseEvent({ ground_truth_action: "maybe" })), "invalid ground_truth_action");
  assert.equal(validateEvent(baseEvent({ trial_number: 0 })), "invalid trial_number");
  assert.equal(validateEvent(baseEvent({ latency_ms: -1 })), "invalid latency_ms");
});

test("qualityForEvent flags attention-check and latency anomalies", () => {
  const q1 = qualityForEvent(baseEvent({ latency_ms: 250 }));
  assert.ok(q1.quality_flags.includes("latency_too_fast"));
  assert.equal(q1.quality_score, 70);

  const q2 = qualityForEvent(
    baseEvent({
      is_attention_check: true,
      attention_check_passed: false,
      latency_ms: 130000,
    }),
  );
  assert.ok(q2.quality_flags.includes("attention_check_failed"));
  assert.ok(q2.quality_flags.includes("latency_too_slow"));
  assert.equal(q2.quality_score, 30);
});

test("toCsv emits header and row values", () => {
  const csv = toCsv([baseEvent()]);
  assert.ok(csv.includes("participant_id"));
  assert.ok(csv.includes("\"p-1\""));
});

test("summarizeSessions marks completed/dropout and include decision", () => {
  const completedEvents = [
    {
      ...baseEvent({
        trial_number: 6,
        total_expected_trials: 6,
        server_timestamp: "2026-03-11T10:30:00.000Z",
        quality_score: 95,
      }),
    },
  ];

  const completedRows = summarizeSessions(completedEvents, {
    nowIso: "2026-03-11T10:31:00.000Z",
    dropoutMinutes: 20,
  });
  assert.equal(completedRows.length, 1);
  assert.equal(completedRows[0].status, "completed");
  assert.equal(completedRows[0].recommended_include, true);

  const dropoutEvents = [
    {
      ...baseEvent({
        trial_number: 2,
        total_expected_trials: 6,
        is_attention_check: true,
        attention_check_passed: false,
        server_timestamp: "2026-03-11T09:00:00.000Z",
        quality_score: 20,
      }),
    },
  ];

  const dropoutRows = summarizeSessions(dropoutEvents, {
    nowIso: "2026-03-11T10:00:00.000Z",
    dropoutMinutes: 20,
  });
  assert.equal(dropoutRows.length, 1);
  assert.equal(dropoutRows[0].status, "dropout");
  assert.equal(dropoutRows[0].recommended_include, false);
  assert.ok(dropoutRows[0].exclude_reasons.includes("attention_check_failed"));
});
