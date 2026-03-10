import assert from "node:assert/strict";
import test from "node:test";
import { createApp } from "../backend/app.js";

function baseEvent(overrides = {}) {
  return {
    session_id: "s-api-1",
    participant_id: "p-api-1",
    condition: "A",
    trial_number: 1,
    scenario_id: "sc-1",
    domain: "financial",
    ai_correct: false,
    is_attention_check: false,
    attention_check_passed: null,
    ground_truth_action: "override",
    decision: "override",
    timestamp: "2026-03-11T11:00:00.000Z",
    latency_ms: 1500,
    total_expected_trials: 6,
    ...overrides,
  };
}

async function withServer(run) {
  const events = [];
  const store = {
    ensureStorage: async () => {},
    appendEvent: async (e) => {
      events.push(e);
    },
    readEvents: async () => events.slice(),
  };

  const app = createApp(store, { dropoutMinutes: 20 });
  const server = await new Promise((resolve) => {
    const s = app.listen(0, () => resolve(s));
  });

  const address = server.address();
  const baseUrl = `http://127.0.0.1:${address.port}`;

  try {
    await run({ baseUrl, events });
  } finally {
    await new Promise((resolve, reject) => server.close((err) => (err ? reject(err) : resolve())));
  }
}

test("GET /api/health returns service status", async () => {
  await withServer(async ({ baseUrl }) => {
    const res = await fetch(`${baseUrl}/api/health`);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.ok, true);
    assert.equal(body.service, "trustlab-logger");
  });
});

test("POST /api/log-event validates payload", async () => {
  await withServer(async ({ baseUrl }) => {
    const res = await fetch(`${baseUrl}/api/log-event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    assert.equal(res.status, 400);
    const body = await res.json();
    assert.equal(body.ok, false);
  });
});

test("POST /api/log-event persists enriched event", async () => {
  await withServer(async ({ baseUrl, events }) => {
    const res = await fetch(`${baseUrl}/api/log-event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(baseEvent()),
    });
    assert.equal(res.status, 201);
    const body = await res.json();
    assert.equal(body.ok, true);
    assert.equal(typeof body.event_id, "string");
    assert.equal(events.length, 1);
    assert.equal(events[0].participant_id, "p-api-1");
    assert.equal(typeof events[0].server_timestamp, "string");
    assert.equal(typeof events[0].quality_score, "number");
  });
});

test("GET /api/events.json and /api/events.csv return exported events", async () => {
  await withServer(async ({ baseUrl }) => {
    await fetch(`${baseUrl}/api/log-event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(baseEvent()),
    });

    const jsonRes = await fetch(`${baseUrl}/api/events.json`);
    assert.equal(jsonRes.status, 200);
    const jsonBody = await jsonRes.json();
    assert.equal(jsonBody.count, 1);

    const csvRes = await fetch(`${baseUrl}/api/events.csv`);
    assert.equal(csvRes.status, 200);
    const csv = await csvRes.text();
    assert.ok(csv.includes("participant_id"));
    assert.ok(csv.includes("p-api-1"));
  });
});

test("GET /api/quality-report.json returns session summary", async () => {
  await withServer(async ({ baseUrl }) => {
    await fetch(`${baseUrl}/api/log-event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(baseEvent({
        trial_number: 6,
        total_expected_trials: 6,
      })),
    });

    const res = await fetch(`${baseUrl}/api/quality-report.json`);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.sessions_count, 1);
    assert.equal(Array.isArray(body.sessions), true);
    assert.equal(body.sessions[0].status, "completed");
  });
});
