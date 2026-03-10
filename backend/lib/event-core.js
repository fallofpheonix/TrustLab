const VALID_CONDITIONS = new Set(["A", "B"]);
const VALID_DECISIONS = new Set(["accept", "override"]);

export function toCsv(events) {
  if (!events.length) return "";
  const headerSet = new Set();
  for (const e of events) {
    for (const k of Object.keys(e)) headerSet.add(k);
  }
  const headers = Array.from(headerSet);
  const escape = (v) => JSON.stringify(v ?? "");
  const rows = events.map((e) => headers.map((h) => escape(e[h])).join(","));
  return [headers.join(","), ...rows].join("\n");
}

export function validateEvent(e) {
  const required = [
    "session_id",
    "participant_id",
    "condition",
    "trial_number",
    "scenario_id",
    "domain",
    "ai_correct",
    "is_attention_check",
    "ground_truth_action",
    "decision",
    "timestamp",
    "latency_ms",
  ];
  for (const field of required) {
    if (!(field in e)) return `missing field: ${field}`;
  }
  if (!VALID_CONDITIONS.has(e.condition)) return "invalid condition";
  if (!VALID_DECISIONS.has(e.decision)) return "invalid decision";
  if (!VALID_DECISIONS.has(e.ground_truth_action)) return "invalid ground_truth_action";
  if (typeof e.trial_number !== "number" || e.trial_number < 1) return "invalid trial_number";
  if (typeof e.latency_ms !== "number" || e.latency_ms < 0) return "invalid latency_ms";
  if (typeof e.ai_correct !== "boolean") return "invalid ai_correct";
  if (typeof e.is_attention_check !== "boolean") return "invalid is_attention_check";
  if (
    !(
      typeof e.attention_check_passed === "boolean" ||
      e.attention_check_passed === null ||
      typeof e.attention_check_passed === "undefined"
    )
  ) {
    return "invalid attention_check_passed";
  }
  if (
    !(
      typeof e.total_expected_trials === "number" ||
      typeof e.total_expected_trials === "undefined"
    )
  ) {
    return "invalid total_expected_trials";
  }
  return null;
}

export function qualityForEvent(e) {
  const flags = [];
  if (e.latency_ms < 400) flags.push("latency_too_fast");
  if (e.latency_ms > 120000) flags.push("latency_too_slow");
  if (e.is_attention_check && e.attention_check_passed === false) flags.push("attention_check_failed");
  if (!VALID_DECISIONS.has(e.decision)) flags.push("decision_invalid");

  let quality_score = 100;
  if (flags.includes("latency_too_fast")) quality_score -= 30;
  if (flags.includes("latency_too_slow")) quality_score -= 10;
  if (flags.includes("attention_check_failed")) quality_score -= 60;
  if (flags.includes("decision_invalid")) quality_score -= 30;
  if (quality_score < 0) quality_score = 0;

  return { quality_flags: flags, quality_score };
}

export function summarizeSessions(events, opts = {}) {
  const dropoutMinutes = Number(opts.dropoutMinutes ?? 20);
  const nowMs = opts.nowIso ? Date.parse(opts.nowIso) : Date.now();
  const sessions = new Map();

  for (const e of events) {
    const key = e.session_id || "unknown";
    if (!sessions.has(key)) {
      sessions.set(key, {
        session_id: key,
        participant_id: e.participant_id ?? null,
        condition: e.condition ?? null,
        total_expected_trials: 0,
        total_events: 0,
        completed_trials: 0,
        attention_failed: false,
        avg_quality_score: 0,
        last_server_timestamp: null,
      });
    }
    const s = sessions.get(key);
    s.total_events += 1;
    s.total_expected_trials = Math.max(s.total_expected_trials, Number(e.total_expected_trials || 0));
    s.completed_trials = Math.max(s.completed_trials, Number(e.trial_number || 0));
    if (e.is_attention_check && e.attention_check_passed === false) s.attention_failed = true;
    const q = typeof e.quality_score === "number" ? e.quality_score : qualityForEvent(e).quality_score;
    s.avg_quality_score += q;
    if (e.server_timestamp) {
      if (!s.last_server_timestamp || Date.parse(e.server_timestamp) > Date.parse(s.last_server_timestamp)) {
        s.last_server_timestamp = e.server_timestamp;
      }
    }
  }

  const rows = [];
  for (const s of sessions.values()) {
    s.avg_quality_score = s.total_events ? Number((s.avg_quality_score / s.total_events).toFixed(2)) : 0;
    const lastMs = s.last_server_timestamp ? Date.parse(s.last_server_timestamp) : nowMs;
    const idleMinutes = (nowMs - lastMs) / 60000;
    const done = s.total_expected_trials > 0 && s.completed_trials >= s.total_expected_trials;
    let status = "in_progress";
    if (done) status = "completed";
    else if (idleMinutes >= dropoutMinutes) status = "dropout";

    const exclude_reasons = [];
    if (s.attention_failed) exclude_reasons.push("attention_check_failed");
    if (s.avg_quality_score < 50) exclude_reasons.push("low_quality_score");

    rows.push({
      ...s,
      status,
      exclude_reasons,
      recommended_include: exclude_reasons.length === 0,
    });
  }
  return rows;
}
