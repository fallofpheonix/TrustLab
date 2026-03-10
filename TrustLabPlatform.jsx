import React, { useState, useEffect, useRef, useCallback } from "react";

// ─── Google Fonts ───────────────────────────────────────────────────────────
const FontLoader = () => (
  <style>{`
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Syne:wght@400;600;700;800&display=swap');
  `}</style>
);

// ─── Design Tokens ───────────────────────────────────────────────────────────
const css = `
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #080c14;
    --bg2:       #0e1520;
    --bg3:       #141d2b;
    --border:    #1e2d42;
    --border2:   #263548;
    --amber:     #f5a623;
    --amber-dim: #c47d0e;
    --cyan:      #3dd6c8;
    --red:       #e05c5c;
    --text:      #d4dde8;
    --text-dim:  #6b7f96;
    --text-mute: #3a4f66;
    --mono:      'DM Mono', monospace;
    --sans:      'Syne', sans-serif;
  }

  html, body, #root { height: 100%; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--mono);
    font-size: 13px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

  /* Noise overlay */
  body::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    opacity: 0.4;
  }

  /* ── Layout ─────────────────────────────────────────────── */
  .app { position: relative; z-index: 1; min-height: 100vh; display: flex; flex-direction: column; }

  .topbar {
    border-bottom: 1px solid var(--border);
    padding: 0 32px;
    height: 52px;
    display: flex; align-items: center; justify-content: space-between;
    background: var(--bg);
    position: sticky; top: 0; z-index: 100;
  }
  .topbar-brand {
    font-family: var(--sans); font-weight: 800; font-size: 15px; letter-spacing: 0.02em;
    color: var(--amber); display: flex; align-items: center; gap: 10px;
  }
  .topbar-brand-dot { width: 7px; height: 7px; background: var(--amber); border-radius: 50%; animation: pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.8)} }
  .topbar-meta { font-size: 11px; color: var(--text-dim); display: flex; gap: 20px; }
  .topbar-meta span { display: flex; align-items: center; gap: 6px; }
  .topbar-meta .dot { width: 5px; height: 5px; border-radius: 50%; background: var(--cyan); }

  .main { flex: 1; padding: 32px; max-width: 960px; margin: 0 auto; width: 100%; }

  /* ── Cards ───────────────────────────────────────────────── */
  .card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
  }
  .card-header {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
  }
  .card-title {
    font-family: var(--sans); font-weight: 700; font-size: 11px;
    letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-dim);
  }
  .card-body { padding: 24px 20px; }

  /* ── Badges ─────────────────────────────────────────────── */
  .badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 8px; border-radius: 2px;
    font-size: 10px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase;
  }
  .badge-amber { background: rgba(245,166,35,.12); color: var(--amber); border: 1px solid rgba(245,166,35,.25); }
  .badge-cyan  { background: rgba(61,214,200,.10); color: var(--cyan);  border: 1px solid rgba(61,214,200,.20); }
  .badge-dim   { background: rgba(107,127,150,.10); color: var(--text-dim); border: 1px solid var(--border); }
  .badge-red   { background: rgba(224,92,92,.12); color: var(--red); border: 1px solid rgba(224,92,92,.25); }

  /* ── Buttons ─────────────────────────────────────────────── */
  .btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    padding: 10px 22px; border-radius: 3px; cursor: pointer;
    font-family: var(--mono); font-size: 12px; font-weight: 500; letter-spacing: 0.05em;
    border: none; transition: all .15s ease; white-space: nowrap;
  }
  .btn-primary {
    background: var(--amber); color: #000;
  }
  .btn-primary:hover { background: #ffc147; transform: translateY(-1px); box-shadow: 0 4px 20px rgba(245,166,35,.3); }
  .btn-primary:active { transform: translateY(0); }
  .btn-ghost {
    background: transparent; color: var(--text-dim);
    border: 1px solid var(--border2);
  }
  .btn-ghost:hover { border-color: var(--amber); color: var(--amber); }
  .btn-danger {
    background: transparent; color: var(--red); border: 1px solid rgba(224,92,92,.3);
  }
  .btn-danger:hover { background: rgba(224,92,92,.1); }
  .btn-lg { padding: 14px 32px; font-size: 13px; }
  .btn-sm { padding: 6px 14px; font-size: 11px; }
  .btn:disabled { opacity: .4; cursor: not-allowed; transform: none !important; }

  /* ── Decision Buttons ─────────────────────────────────────── */
  .decision-btn {
    flex: 1; padding: 20px 24px; border-radius: 3px; cursor: pointer;
    font-family: var(--mono); font-size: 13px; font-weight: 500;
    border: 1.5px solid; transition: all .2s ease;
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    position: relative; overflow: hidden;
  }
  .decision-btn::before {
    content: ''; position: absolute; inset: 0;
    opacity: 0; transition: opacity .2s;
  }
  .decision-btn:hover::before { opacity: 1; }
  .decision-btn-accept {
    background: rgba(61,214,200,.06); border-color: rgba(61,214,200,.3); color: var(--cyan);
  }
  .decision-btn-accept::before { background: rgba(61,214,200,.06); }
  .decision-btn-accept:hover { border-color: var(--cyan); box-shadow: 0 0 24px rgba(61,214,200,.15); transform: translateY(-2px); }
  .decision-btn-override {
    background: rgba(224,92,92,.06); border-color: rgba(224,92,92,.3); color: var(--red);
  }
  .decision-btn-override::before { background: rgba(224,92,92,.06); }
  .decision-btn-override:hover { border-color: var(--red); box-shadow: 0 0 24px rgba(224,92,92,.15); transform: translateY(-2px); }
  .decision-btn-label { font-family: var(--sans); font-weight: 700; font-size: 15px; letter-spacing: 0.02em; }
  .decision-btn-sub { font-size: 10px; opacity: .6; letter-spacing: 0.06em; }
  .decision-btn:disabled { opacity: .3; cursor: not-allowed; transform: none !important; box-shadow: none !important; }

  /* ── Forms ───────────────────────────────────────────────── */
  .field { display: flex; flex-direction: column; gap: 8px; }
  .label { font-size: 11px; color: var(--text-dim); letter-spacing: 0.08em; text-transform: uppercase; }
  .input {
    background: var(--bg3); border: 1px solid var(--border2); border-radius: 3px;
    color: var(--text); font-family: var(--mono); font-size: 13px;
    padding: 10px 14px; outline: none; transition: border-color .15s;
    width: 100%;
  }
  .input:focus { border-color: var(--amber); }
  .input::placeholder { color: var(--text-mute); }

  /* ── Progress bar ────────────────────────────────────────── */
  .progress-track {
    height: 2px; background: var(--border); border-radius: 1px; overflow: hidden;
  }
  .progress-fill {
    height: 100%; background: var(--amber); border-radius: 1px;
    transition: width .4s cubic-bezier(.4,0,.2,1);
  }

  /* ── Confidence Meter ────────────────────────────────────── */
  .conf-track {
    height: 6px; background: var(--bg3); border-radius: 3px; overflow: hidden;
    border: 1px solid var(--border);
  }
  .conf-fill {
    height: 100%; border-radius: 3px;
    transition: width .6s cubic-bezier(.4,0,.2,1);
  }

  /* ── Data Table ──────────────────────────────────────────── */
  .data-table { width: 100%; border-collapse: collapse; font-size: 12px; }
  .data-table th {
    text-align: left; padding: 8px 12px; font-size: 10px;
    letter-spacing: .1em; text-transform: uppercase; color: var(--text-mute);
    border-bottom: 1px solid var(--border); font-weight: 500;
  }
  .data-table td {
    padding: 9px 12px; border-bottom: 1px solid rgba(30,45,66,.5);
    font-size: 11.5px; color: var(--text);
  }
  .data-table tr:last-child td { border-bottom: none; }
  .data-table tr:hover td { background: rgba(255,255,255,.02); }

  /* ── Stat Grid ───────────────────────────────────────────── */
  .stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: var(--border); }
  .stat-cell {
    background: var(--bg2); padding: 20px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .stat-value {
    font-family: var(--sans); font-weight: 800; font-size: 28px;
    letter-spacing: -.02em; line-height: 1;
  }
  .stat-label { font-size: 10px; color: var(--text-dim); letter-spacing: .08em; text-transform: uppercase; }
  .stat-sub { font-size: 10px; color: var(--text-mute); }

  /* ── Misc ────────────────────────────────────────────────── */
  .divider { height: 1px; background: var(--border); margin: 20px 0; }
  .mono { font-family: var(--mono); }
  .amber { color: var(--amber); }
  .cyan  { color: var(--cyan); }
  .red   { color: var(--red); }
  .dim   { color: var(--text-dim); }
  .mute  { color: var(--text-mute); }

  /* ── Animations ──────────────────────────────────────────── */
  @keyframes fadeUp {
    from { opacity:0; transform: translateY(16px); }
    to   { opacity:1; transform: translateY(0); }
  }
  @keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
  @keyframes scanline {
    0%   { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
  }
  .fade-up { animation: fadeUp .4s ease forwards; }
  .fade-up-2 { animation: fadeUp .4s .1s ease both; }
  .fade-up-3 { animation: fadeUp .4s .2s ease both; }
  .fade-up-4 { animation: fadeUp .4s .3s ease both; }

  /* ── Recommendation Box ──────────────────────────────────── */
  .rec-box {
    background: var(--bg3); border: 1px solid var(--border2); border-radius: 4px;
    padding: 24px; position: relative; overflow: hidden;
  }
  .rec-box::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--amber), var(--cyan));
  }
  .rec-agent { font-size: 11px; color: var(--text-dim); letter-spacing: .08em; text-transform: uppercase; margin-bottom: 12px; }
  .rec-content { font-family: var(--sans); font-weight: 600; font-size: 18px; color: var(--text); line-height: 1.4; }
  .rec-rationale { font-size: 12px; color: var(--text-dim); margin-top: 10px; line-height: 1.6; }

  /* ── Nav Tabs ────────────────────────────────────────────── */
  .tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border); }
  .tab {
    padding: 12px 20px; cursor: pointer; font-size: 11px;
    letter-spacing: .08em; text-transform: uppercase; color: var(--text-dim);
    border-bottom: 2px solid transparent; margin-bottom: -1px;
    transition: all .15s; font-family: var(--mono);
  }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--amber); border-bottom-color: var(--amber); }

  /* ── JSON viewer ─────────────────────────────────────────── */
  .json-block {
    background: var(--bg); border: 1px solid var(--border); border-radius: 3px;
    padding: 16px; font-size: 11px; line-height: 1.7; overflow-x: auto;
    white-space: pre-wrap; word-break: break-all; color: var(--text-dim);
    max-height: 320px; overflow-y: auto;
  }
  .json-key { color: var(--cyan); }
  .json-str { color: #b5c8e0; }
  .json-num { color: var(--amber); }

  /* ── Latency Bar ─────────────────────────────────────────── */
  .latency-bar { display: flex; align-items: center; gap: 10px; }
  .latency-fill { height: 3px; border-radius: 2px; background: var(--amber); min-width: 2px; transition: width .4s; }

  /* ── Onboarding ──────────────────────────────────────────── */
  .onboard-hero {
    text-align: center; padding: 48px 24px 40px;
  }
  .onboard-title {
    font-family: var(--sans); font-weight: 800; font-size: 36px;
    letter-spacing: -.02em; line-height: 1.1; margin-bottom: 14px;
  }
  .onboard-sub { font-size: 13px; color: var(--text-dim); line-height: 1.7; max-width: 480px; margin: 0 auto; }

  /* ── Rating Scale ────────────────────────────────────────── */
  .rating-scale { display: flex; gap: 8px; }
  .rating-btn {
    flex: 1; padding: 10px 6px; border-radius: 2px; cursor: pointer;
    background: var(--bg3); border: 1px solid var(--border2); color: var(--text-dim);
    font-family: var(--mono); font-size: 12px; font-weight: 500;
    transition: all .15s; text-align: center;
  }
  .rating-btn:hover { border-color: var(--amber); color: var(--amber); }
  .rating-btn.selected { background: rgba(245,166,35,.15); border-color: var(--amber); color: var(--amber); }

  /* ── Empty state ─────────────────────────────────────────── */
  .empty { text-align: center; padding: 48px; color: var(--text-mute); font-size: 12px; }
  .empty-icon { font-size: 28px; margin-bottom: 12px; opacity: .4; }

  /* ── Download Button ─────────────────────────────────────── */
  .dl-row { display: flex; gap: 10px; flex-wrap: wrap; }

  /* ── Grid helpers ────────────────────────────────────────── */
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
  .stack { display: flex; flex-direction: column; gap: 16px; }
  .row { display: flex; align-items: center; gap: 12px; }
  .row-between { display: flex; align-items: center; justify-content: space-between; }
  .mt8  { margin-top: 8px; }
  .mt16 { margin-top: 16px; }
  .mt24 { margin-top: 24px; }

  @media (max-width: 640px) {
    .stat-grid { grid-template-columns: 1fr 1fr; }
    .grid-2 { grid-template-columns: 1fr; }
    .main { padding: 16px; }
    .topbar { padding: 0 16px; }
  }
`;

// ─── Scenario Bank ─────────────────────────────────────────────────────────
const SCENARIOS = [
  {
    id: "s1", domain: "Medical",
    context: "Patient presents with persistent fatigue, mild fever for 10 days, elevated WBC count.",
    recommendation: "Order a complete blood panel and refer to infectious disease specialist.",
    rationale: "Symptom pattern and lab values are consistent with early-stage systemic infection requiring specialist evaluation.",
    ai_accuracy_hint: 0.84,
    ai_correct: true,
  },
  {
    id: "s2", domain: "Financial",
    context: "Market volatility index at 28. Client portfolio is 70% equities, 5-year horizon.",
    recommendation: "Reduce equity exposure to 55% and increase bonds to stabilize near-term risk.",
    rationale: "Current volatility exceeds 5-year average. Rebalancing now protects downside while maintaining long-term growth potential.",
    ai_accuracy_hint: 0.71,
    ai_correct: false,
  },
  {
    id: "s3", domain: "Product",
    context: "E-commerce checkout abandonment rate increased 12% this month. Cart average is $94.",
    recommendation: "Implement one-click checkout and add trust badges at payment step.",
    rationale: "Abandonment spikes at payment page correlate strongly with friction. Trust signals reduce hesitation for mid-range purchases.",
    ai_accuracy_hint: 0.78,
    ai_correct: true,
  },
  {
    id: "ac1", domain: "Attention Check",
    context: "Attention check: to confirm careful reading, select OVERRIDE for this trial.",
    recommendation: "Accept this recommendation for the current trial.",
    rationale: "This trial validates response quality and should be overridden.",
    ai_accuracy_hint: 0.99,
    ai_correct: false,
    is_attention_check: true,
  },
  {
    id: "s4", domain: "Logistics",
    context: "Supply chain disruption: primary supplier delayed 3 weeks. Q3 launch at risk.",
    recommendation: "Activate backup supplier contract and expedite air freight for critical components.",
    rationale: "Delay cost analysis favors expedited shipping over launch postponement. Backup supplier quality metrics within acceptable range.",
    ai_accuracy_hint: 0.88,
    ai_correct: true,
  },
  {
    id: "s5", domain: "Security",
    context: "Unusual login attempts detected: 240 failed auths from 3 IPs over 6 hours.",
    recommendation: "Temporarily block the flagged IPs and require 2FA for all admin accounts.",
    rationale: "Activity pattern matches credential stuffing profile. Blocking is low-risk; 2FA prevents escalation if any credential was valid.",
    ai_accuracy_hint: 0.93,
    ai_correct: true,
  },
  {
    id: "s6", domain: "HR",
    context: "Two finalists for senior engineer role. Candidate A: 8yr exp, strong technical. Candidate B: 5yr exp, high culture fit scores.",
    recommendation: "Advance Candidate A to final round given role's technical complexity.",
    rationale: "Role requires immediate senior-level output. Technical depth outweighs culture fit at this seniority tier for productivity timeline.",
    ai_accuracy_hint: 0.67,
    ai_correct: false,
  },
];

// ─── Condition Configs ──────────────────────────────────────────────────────
const CONDITIONS = {
  A: {
    agent_name: "AI Assistant",
    tone: "formal",
    confidence_style: "probability",
    label: "Condition A — Formal / Probability",
  },
  B: {
    agent_name: "Alex",
    tone: "conversational",
    confidence_style: "certainty",
    label: "Condition B — Conversational / Certainty",
  },
};

// ─── Helpers ────────────────────────────────────────────────────────────────
const PARTICIPANT_ID_KEY = "trustlab.participant_id";
const uuid = () => {
  if (typeof crypto !== "undefined" && crypto.randomUUID) return crypto.randomUUID();
  return "id-" + Math.random().toString(36).slice(2) + Date.now().toString(36);
};
const now_ts = () => new Date().toISOString();
const hashString = (s) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
  }
  return h >>> 0;
};
const assignCondition = (participantId) => (hashString(participantId) % 2 === 0 ? "A" : "B");
const getOrCreateParticipantId = () => {
  try {
    const existing = localStorage.getItem(PARTICIPANT_ID_KEY);
    if (existing) return existing;
    const id = "p-" + uuid().slice(0, 8).toUpperCase();
    localStorage.setItem(PARTICIPANT_ID_KEY, id);
    return id;
  } catch {
    return "p-" + uuid().slice(0, 8).toUpperCase();
  }
};
async function postLogEvent(event) {
  try {
    const res = await fetch("/api/log-event", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(event),
    });
    if (!res.ok) throw new Error("non-2xx");
    const body = await res.json();
    return { ok: true, server_timestamp: body.server_timestamp || null, event_id: body.event_id || null };
  } catch {
    return { ok: false, server_timestamp: null, event_id: null };
  }
}

function formatConfidence(value, style) {
  if (style === "probability") return `${Math.round(value * 100)}% probability`;
  const v = value;
  if (v >= 0.9) return "Highly certain";
  if (v >= 0.75) return "Fairly confident";
  if (v >= 0.6) return "Moderately confident";
  return "Uncertain";
}

function confColor(value) {
  if (value >= 0.85) return "var(--cyan)";
  if (value >= 0.7) return "var(--amber)";
  return "var(--red)";
}

function logsToCSV(logs) {
  const headers = [
    "session_id",
    "participant_id",
    "condition",
    "trial_number",
    "scenario_id",
    "domain",
    "ai_correct",
    "is_attention_check",
    "attention_check_passed",
    "ground_truth_action",
    "decision",
    "confidence_rating",
    "baseline_ai_trust",
    "ai_familiarity",
    "ai_usage_frequency",
    "timestamp",
    "server_timestamp",
    "latency_ms",
    "sync_status",
  ];
  const rows = logs.map(l =>
    headers.map(h => JSON.stringify(l[h] ?? "")).join(",")
  );
  return [headers.join(","), ...rows].join("\n");
}

function downloadText(content, filename, type = "text/plain") {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

// ─── JSON Renderer ──────────────────────────────────────────────────────────
function JsonView({ data }) {
  const raw = JSON.stringify(data, null, 2);
  const html = raw
    .replace(/("[\w_]+"):/g, '<span class="json-key">$1</span>:')
    .replace(/: (".*?")/g, ': <span class="json-str">$1</span>')
    .replace(/: (\d+\.?\d*)/g, ': <span class="json-num">$1</span>');
  return <pre className="json-block" dangerouslySetInnerHTML={{ __html: html }} />;
}

// ─── PHASE 1: Onboarding ────────────────────────────────────────────────────
function PhaseOnboard({ onStart }) {
  const [name, setName] = useState("");
  const [consent, setConsent] = useState(false);
  const [baselineTrust, setBaselineTrust] = useState("");
  const [aiFamiliarity, setAiFamiliarity] = useState("");
  const [aiUsageFrequency, setAiUsageFrequency] = useState("");
  const surveyComplete = baselineTrust && aiFamiliarity && aiUsageFrequency;

  return (
    <div className="fade-up">
      <div className="onboard-hero">
        <div className="onboard-title">
          Human–AI<br /><span className="amber">Trust Calibration</span><br />Lab
        </div>
        <p className="onboard-sub mt8">
          A controlled behavioral experiment measuring reliance patterns
          across interface cue conditions.
        </p>
      </div>

      <div className="card fade-up-2">
        <div className="card-header">
          <span className="card-title">Participant Registration</span>
          <span className="badge badge-amber">Phase 1 / 6</span>
        </div>
        <div className="card-body stack">
          <div className="field">
            <label className="label">Display Name (optional)</label>
            <input
              className="input"
              placeholder="Anonymous"
              value={name}
              onChange={e => setName(e.target.value)}
            />
          </div>

          <div className="card" style={{ background: "var(--bg3)" }}>
            <div className="card-body" style={{ fontSize: "12px", color: "var(--text-dim)", lineHeight: "1.8" }}>
              <strong style={{ color: "var(--text)" }}>Study Information</strong><br />
              You will be presented with several scenarios across different domains.
              For each scenario, an AI system will provide a recommendation.
              You will decide to <strong style={{ color: "var(--cyan)" }}>Accept</strong> or <strong style={{ color: "var(--red)" }}>Override</strong> that recommendation.
              Some recommendations are correct and some are incorrect.
              Your decision latency and choices are recorded for research purposes.
              The session takes approximately 5–10 minutes.
            </div>
          </div>

          <div className="card" style={{ background: "var(--bg3)" }}>
            <div className="card-header">
              <span className="card-title">Baseline Trust Mini-Survey</span>
            </div>
            <div className="card-body stack">
              <div className="field">
                <label className="label">Baseline Trust In AI (1-5)</label>
                <select className="input" value={baselineTrust} onChange={(e) => setBaselineTrust(e.target.value)}>
                  <option value="">Select</option>
                  {[1, 2, 3, 4, 5].map((n) => <option key={n} value={String(n)}>{n}</option>)}
                </select>
              </div>
              <div className="field">
                <label className="label">AI Familiarity (1-5)</label>
                <select className="input" value={aiFamiliarity} onChange={(e) => setAiFamiliarity(e.target.value)}>
                  <option value="">Select</option>
                  {[1, 2, 3, 4, 5].map((n) => <option key={n} value={String(n)}>{n}</option>)}
                </select>
              </div>
              <div className="field">
                <label className="label">AI Usage Frequency</label>
                <select className="input" value={aiUsageFrequency} onChange={(e) => setAiUsageFrequency(e.target.value)}>
                  <option value="">Select</option>
                  <option value="rarely">Rarely</option>
                  <option value="weekly">Weekly</option>
                  <option value="daily">Daily</option>
                </select>
              </div>
            </div>
          </div>

          <label
            style={{ display: "flex", alignItems: "flex-start", gap: "12px", cursor: "pointer" }}
            onClick={() => setConsent(!consent)}
          >
            <div
              style={{
                width: 18, height: 18, marginTop: 2, flexShrink: 0,
                border: `1.5px solid ${consent ? "var(--amber)" : "var(--border2)"}`,
                background: consent ? "rgba(245,166,35,.2)" : "transparent",
                borderRadius: 2, display: "flex", alignItems: "center", justifyContent: "center",
                cursor: "pointer", transition: "all .15s",
              }}
            >
              {consent && <span style={{ color: "var(--amber)", fontSize: 11, fontWeight: 700 }}>✓</span>}
            </div>
            <span style={{ fontSize: 12, color: "var(--text-dim)", lineHeight: 1.6 }}>
              I understand that my anonymous interaction data will be recorded and used for research.
              I consent to participate voluntarily and may stop at any time.
            </span>
          </label>

          <button
            className="btn btn-primary btn-lg"
            disabled={!consent || !surveyComplete}
            onClick={() => onStart({
              name: name || "Anonymous",
              baseline: {
                baseline_ai_trust: Number(baselineTrust),
                ai_familiarity: Number(aiFamiliarity),
                ai_usage_frequency: aiUsageFrequency,
              },
            })}
          >
            Begin Experiment →
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── PHASE 2 + 3: Condition Assignment Display ──────────────────────────────
function PhaseCondition({ participant, onContinue }) {
  const cond = CONDITIONS[participant.condition];

  return (
    <div className="fade-up">
      <div className="card">
        <div className="card-header">
          <span className="card-title">Session Initialized</span>
          <span className="badge badge-cyan">Phase 2 / 6</span>
        </div>
        <div className="card-body stack">
          <div className="row-between">
            <div>
              <div style={{ fontSize: 11, color: "var(--text-dim)", textTransform: "uppercase", letterSpacing: ".08em", marginBottom: 6 }}>Participant ID</div>
              <div style={{ fontFamily: "var(--mono)", fontSize: 18, fontWeight: 500, color: "var(--amber)", letterSpacing: ".05em" }}>{participant.id}</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 11, color: "var(--text-dim)", textTransform: "uppercase", letterSpacing: ".08em", marginBottom: 6 }}>Assigned Condition</div>
              <span className="badge badge-amber" style={{ fontSize: 13, padding: "5px 12px" }}>
                {participant.condition}
              </span>
            </div>
          </div>

          <div className="divider" />

          <div style={{ fontSize: 12, color: "var(--text-dim)", marginBottom: 4 }}>Interface Configuration</div>
          <div className="card" style={{ background: "var(--bg3)" }}>
            <div className="card-body">
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
                {[
                  ["Agent Name", cond.agent_name],
                  ["Tone", cond.tone],
                  ["Confidence Style", cond.confidence_style],
                ].map(([k, v]) => (
                  <div key={k} style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                    <div style={{ fontSize: 10, color: "var(--text-mute)", textTransform: "uppercase", letterSpacing: ".08em" }}>{k}</div>
                    <div style={{ fontSize: 13, color: "var(--cyan)" }}>{v}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div style={{ fontSize: 11, color: "var(--text-mute)", lineHeight: 1.7 }}>
            ⚠ Condition assignment is deterministic by participant ID hash and blinded. You will interact with a simulated AI interface
            configured to your assigned condition parameters throughout all scenarios.
          </div>

          <button className="btn btn-primary" onClick={onContinue}>
            Proceed to Task →
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── PHASE 4: Task Engine ───────────────────────────────────────────────────
function PhaseTask({ participant, onComplete }) {
  const cond = CONDITIONS[participant.condition];
  const [trialIdx, setTrialIdx] = useState(0);
  const [decision, setDecision] = useState(null);
  const [rating, setRating] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const [logs, setLogs] = useState([]);
  const [animKey, setAnimKey] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const scenario = SCENARIOS[trialIdx];
  const total = SCENARIOS.length;
  const progress = trialIdx / total;

  useEffect(() => {
    setStartTime(Date.now());
    setDecision(null);
    setRating(null);
    setAnimKey(k => k + 1);
  }, [trialIdx]);

  const handleDecision = (d) => {
    if (decision) return;
    setDecision(d);
  };

  const handleSubmit = async () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    const latency = Date.now() - startTime;
    const isAttentionCheck = !!scenario.is_attention_check;
    const groundTruthAction = isAttentionCheck ? "override" : (scenario.ai_correct ? "accept" : "override");
    const attentionCheckPassed = isAttentionCheck ? decision === "override" : null;
    const entry = {
      session_id: participant.session_id,
      participant_id: participant.id,
      condition: participant.condition,
      trial_number: trialIdx + 1,
      scenario_id: scenario.id,
      domain: scenario.domain,
      ai_correct: scenario.ai_correct,
      is_attention_check: isAttentionCheck,
      attention_check_passed: attentionCheckPassed,
      ground_truth_action: groundTruthAction,
      decision,
      confidence_rating: rating,
      baseline_ai_trust: participant.baseline?.baseline_ai_trust ?? null,
      ai_familiarity: participant.baseline?.ai_familiarity ?? null,
      ai_usage_frequency: participant.baseline?.ai_usage_frequency ?? null,
      timestamp: now_ts(),
      latency_ms: latency,
    };
    const sync = await postLogEvent(entry);
    const syncedEntry = {
      ...entry,
      server_timestamp: sync.server_timestamp,
      event_id: sync.event_id,
      sync_status: sync.ok ? "synced" : "pending",
    };
    const newLogs = [...logs, syncedEntry];
    setLogs(newLogs);

    if (trialIdx + 1 >= total) {
      onComplete(newLogs);
    } else {
      setTrialIdx(i => i + 1);
    }
    setIsSubmitting(false);
  };

  const confValue = scenario.ai_accuracy_hint;

  return (
    <div>
      {/* Progress */}
      <div style={{ marginBottom: 24 }}>
        <div className="row-between" style={{ marginBottom: 8 }}>
          <span style={{ fontSize: 11, color: "var(--text-dim)" }}>
            Trial <span className="amber">{trialIdx + 1}</span> / {total}
          </span>
          <div style={{ display: "flex", gap: 8 }}>
            <span className="badge badge-dim">{scenario.domain}</span>
            {scenario.is_attention_check && <span className="badge badge-red">Attention Check</span>}
          </div>
        </div>
        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${progress * 100}%` }} />
        </div>
      </div>

      <div key={animKey} className="fade-up stack">
        {/* Context */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Scenario Context</span>
            <span style={{ fontSize: 10, color: "var(--text-mute)" }}>READ CAREFULLY</span>
          </div>
          <div className="card-body">
            <p style={{ fontSize: 13, color: "var(--text-dim)", lineHeight: 1.8 }}>{scenario.context}</p>
          </div>
        </div>

        {/* AI Recommendation */}
        <div className="rec-box fade-up-2">
          <div className="rec-agent">
            {cond.tone === "conversational"
              ? `${cond.agent_name} suggests`
              : `${cond.agent_name} — Recommendation`}
          </div>
          <div className="rec-content">{scenario.recommendation}</div>
          {cond.tone === "conversational"
            ? <div className="rec-rationale">Here's my thinking: {scenario.rationale}</div>
            : <div className="rec-rationale">Rationale: {scenario.rationale}</div>
          }

          {/* Confidence */}
          <div style={{ marginTop: 20 }}>
            <div className="row-between" style={{ marginBottom: 8 }}>
              <span style={{ fontSize: 10, color: "var(--text-dim)", textTransform: "uppercase", letterSpacing: ".08em" }}>
                Confidence
              </span>
              <span style={{ fontSize: 12, color: confColor(confValue), fontWeight: 500 }}>
                {formatConfidence(confValue, cond.confidence_style)}
              </span>
            </div>
            <div className="conf-track">
              <div
                className="conf-fill"
                style={{
                  width: `${confValue * 100}%`,
                  background: `linear-gradient(90deg, ${confColor(confValue)}88, ${confColor(confValue)})`,
                }}
              />
            </div>
          </div>
        </div>

        {/* Decision */}
        <div className="fade-up-3">
          <div style={{ fontSize: 11, color: "var(--text-dim)", textTransform: "uppercase", letterSpacing: ".08em", marginBottom: 12 }}>
            Your Decision
          </div>
          <div style={{ display: "flex", gap: 12 }}>
            <button
              className={`decision-btn decision-btn-accept ${decision === "accept" ? "selected" : ""}`}
              style={decision === "accept" ? { borderColor: "var(--cyan)", background: "rgba(61,214,200,.12)" } : {}}
              onClick={() => handleDecision("accept")}
              disabled={!!decision}
            >
              <span className="decision-btn-label">Accept</span>
              <span className="decision-btn-sub">Follow the recommendation</span>
            </button>
            <button
              className={`decision-btn decision-btn-override ${decision === "override" ? "selected" : ""}`}
              style={decision === "override" ? { borderColor: "var(--red)", background: "rgba(224,92,92,.12)" } : {}}
              onClick={() => handleDecision("override")}
              disabled={!!decision}
            >
              <span className="decision-btn-label">Override</span>
              <span className="decision-btn-sub">Reject the recommendation</span>
            </button>
          </div>
        </div>

        {/* Confidence Rating */}
        {decision && (
          <div className="card fade-in fade-up-4" style={{ animation: "fadeUp .3s ease" }}>
            <div className="card-header">
              <span className="card-title">Confidence Rating (Optional)</span>
            </div>
            <div className="card-body">
              <div style={{ fontSize: 12, color: "var(--text-dim)", marginBottom: 12 }}>
                How confident are you in your decision?
              </div>
              <div className="rating-scale">
                {[1, 2, 3, 4, 5].map(n => (
                  <button
                    key={n}
                    className={`rating-btn ${rating === n ? "selected" : ""}`}
                    onClick={() => setRating(n)}
                  >
                    {n}
                  </button>
                ))}
              </div>
              <div className="row-between mt8" style={{ fontSize: 10, color: "var(--text-mute)" }}>
                <span>Not at all confident</span>
                <span>Extremely confident</span>
              </div>
            </div>
          </div>
        )}

        {decision && (
          <button
            className="btn btn-primary fade-up"
            onClick={handleSubmit}
            disabled={isSubmitting}
            style={{ animation: "fadeUp .3s .1s ease both" }}
          >
            {trialIdx + 1 >= total ? "Complete Experiment →" : `Next Scenario (${trialIdx + 2}/${total}) →`}
          </button>
        )}
      </div>
    </div>
  );
}

// ─── PHASE 5 + 6: Results, Logs, Export ────────────────────────────────────
function PhaseResults({ participant, logs, onReset }) {
  const [tab, setTab] = useState("stats");
  const cond = CONDITIONS[participant.condition];

  // Compute stats
  const analyticLogs = logs.filter((l) => !l.is_attention_check);
  const attentionLogs = logs.filter((l) => l.is_attention_check);
  const attentionPassed = attentionLogs.length > 0 ? attentionLogs.every((l) => l.attention_check_passed) : null;
  const total = analyticLogs.length;
  const accepted = analyticLogs.filter(l => l.decision === "accept").length;
  const overridden = total - accepted;
  const relianceRate = total > 0 ? (accepted / total) : 0;
  const overrideRate = total > 0 ? (overridden / total) : 0;
  const meanLatency = total > 0 ? Math.round(analyticLogs.reduce((s, l) => s + l.latency_ms, 0) / total) : 0;
  const avgRating = analyticLogs.filter(l => l.confidence_rating).length > 0
    ? (analyticLogs.filter(l => l.confidence_rating).reduce((s, l) => s + l.confidence_rating, 0) / analyticLogs.filter(l => l.confidence_rating).length).toFixed(2)
    : "N/A";

  const handleDownloadJSON = () => {
    const export_data = {
      metadata: {
        session_id: participant.session_id,
        participant_id: participant.id,
        participant_name: participant.name,
        baseline: participant.baseline,
        condition: participant.condition,
        condition_config: cond,
        session_start: logs[0]?.timestamp,
        session_end: logs[logs.length - 1]?.timestamp,
        total_trials: logs.length,
        analytical_trials: total,
        attention_checks: attentionLogs.length,
      },
      summary: {
        reliance_rate: relianceRate,
        override_rate: overrideRate,
        mean_latency_ms: meanLatency,
        avg_confidence_rating: avgRating,
        attention_check_passed: attentionPassed,
      },
      trials: logs,
    };
    downloadText(JSON.stringify(export_data, null, 2), `trustlab_${participant.id}.json`, "application/json");
  };

  const handleDownloadCSV = () => {
    downloadText(logsToCSV(logs), `trustlab_${participant.id}.csv`, "text/csv");
  };

  return (
    <div className="fade-up stack">
      <div className="card">
        <div className="card-header">
          <span className="card-title">Session Complete</span>
          <span className="badge badge-cyan">Phase 5–6 / 6</span>
        </div>

        {/* Stats */}
        <div className="stat-grid">
          <div className="stat-cell">
            <div className="stat-value amber">{(relianceRate * 100).toFixed(0)}%</div>
            <div className="stat-label">Reliance Rate</div>
            <div className="stat-sub">{accepted} accepted / {total}</div>
          </div>
          <div className="stat-cell">
            <div className="stat-value red">{(overrideRate * 100).toFixed(0)}%</div>
            <div className="stat-label">Override Rate</div>
            <div className="stat-sub">{overridden} overridden / {total}</div>
          </div>
          <div className="stat-cell">
            <div className="stat-value cyan">{(meanLatency / 1000).toFixed(1)}s</div>
            <div className="stat-label">Mean Latency</div>
            <div className="stat-sub">{meanLatency}ms avg</div>
          </div>
          <div className="stat-cell">
            <div className="stat-value" style={{ color: "var(--text)" }}>{avgRating}</div>
            <div className="stat-label">Avg. Confidence</div>
            <div className="stat-sub">self-reported (1–5)</div>
          </div>
        </div>
        <div style={{ padding: "12px 20px", borderTop: "1px solid var(--border)", fontSize: 11, color: "var(--text-dim)" }}>
          Attention check:
          {" "}
          <span className={attentionPassed ? "cyan" : "red"}>
            {attentionPassed === null ? "Not present" : (attentionPassed ? "Passed" : "Failed")}
          </span>
          {" · "}
          Baseline trust:
          {" "}
          <span className="amber">{participant.baseline?.baseline_ai_trust ?? "N/A"}/5</span>
        </div>

        {/* Tabs */}
        <div className="tabs" style={{ padding: "0 20px" }}>
          {[
            ["stats", "Per-Trial"],
            ["logs", "Raw Logs"],
            ["export", "Export"],
          ].map(([id, label]) => (
            <div key={id} className={`tab ${tab === id ? "active" : ""}`} onClick={() => setTab(id)}>
              {label}
            </div>
          ))}
        </div>

        <div className="card-body">
          {tab === "stats" && (
            <div>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Domain</th>
                    <th>Decision</th>
                    <th>Latency</th>
                    <th>Conf. Rating</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((l, i) => (
                    <tr key={i}>
                      <td className="mute">{i + 1}</td>
                      <td>{l.domain}</td>
                      <td>
                        <span className={l.decision === "accept" ? "cyan" : "red"}>
                          {l.decision === "accept" ? "✓ Accept" : "✕ Override"}
                        </span>
                      </td>
                      <td>
                        <div className="latency-bar">
                          <span className="amber" style={{ fontWeight: 500 }}>{(l.latency_ms / 1000).toFixed(2)}s</span>
                          <div className="latency-fill" style={{ width: Math.min(60, l.latency_ms / 200) + "px" }} />
                        </div>
                      </td>
                      <td className={l.confidence_rating ? "amber" : "mute"}>
                        {l.confidence_rating ? `${l.confidence_rating}/5` : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {tab === "logs" && (
            <div>
              <div style={{ marginBottom: 12, fontSize: 11, color: "var(--text-dim)" }}>
                Structured event log — {logs.length} records
              </div>
              <JsonView data={logs} />
            </div>
          )}

          {tab === "export" && (
            <div className="stack">
              <div style={{ fontSize: 12, color: "var(--text-dim)", lineHeight: 1.8 }}>
                Export your session dataset for offline statistical analysis.
                JSON includes full metadata and trial records.
                CSV is formatted for pandas / R import.
              </div>

              <div className="card" style={{ background: "var(--bg3)" }}>
                <div className="card-body">
                  <div style={{ fontSize: 11, color: "var(--text-mute)", textTransform: "uppercase", letterSpacing: ".08em", marginBottom: 10 }}>
                    Export Preview (JSON)
                  </div>
                  <JsonView data={{
                    metadata: {
                      participant_id: participant.id,
                      session_id: participant.session_id,
                      condition: participant.condition,
                    },
                    summary: { reliance_rate: relianceRate.toFixed(3), override_rate: overrideRate.toFixed(3), mean_latency_ms: meanLatency },
                    trials: logs.length + " records",
                  }} />
                </div>
              </div>

              <div className="dl-row">
                <button className="btn btn-primary" onClick={handleDownloadJSON}>
                  ↓ Download JSON
                </button>
                <button className="btn btn-ghost" onClick={handleDownloadCSV}>
                  ↓ Download CSV
                </button>
              </div>

              <div className="divider" />

              <div style={{ fontSize: 11, color: "var(--text-mute)" }}>
                Analysis pipeline tip: load CSV with{" "}
                <code style={{ color: "var(--cyan)", background: "rgba(61,214,200,.08)", padding: "1px 5px", borderRadius: 2 }}>
                  pd.read_csv("trustlab_{participant.id}.csv")
                </code>{" "}
                then compute reliance rate by condition using{" "}
                <code style={{ color: "var(--cyan)", background: "rgba(61,214,200,.08)", padding: "1px 5px", borderRadius: 2 }}>
                  df.groupby("condition")["decision"].value_counts(normalize=True)
                </code>
              </div>
            </div>
          )}
        </div>
      </div>

      <button className="btn btn-ghost" onClick={onReset}>
        ↺ Run New Session
      </button>
    </div>
  );
}

// ─── Top Bar ────────────────────────────────────────────────────────────────
function TopBar({ participant, phase }) {
  const phaseLabels = ["", "Onboarding", "Session Init", "Task", "Task", "Results", "Results"];
  return (
    <div className="topbar">
      <div className="topbar-brand">
        <div className="topbar-brand-dot" />
        TrustLab
      </div>
      <div className="topbar-meta">
        {participant && (
          <>
            <span><span className="dot" />{participant.id}</span>
            <span>Cond. {participant.condition}</span>
          </>
        )}
        <span style={{ color: "var(--text-mute)" }}>{phaseLabels[phase] || ""}</span>
      </div>
    </div>
  );
}

// ─── ROOT ────────────────────────────────────────────────────────────────────
export default function App() {
  const [phase, setPhase] = useState(1);
  const [participant, setParticipant] = useState(null);
  const [sessionLogs, setSessionLogs] = useState([]);

  const handleStart = ({ name, baseline }) => {
    const participantId = getOrCreateParticipantId();
    const p = {
      id: participantId,
      name,
      baseline,
      condition: assignCondition(participantId),
      session_id: "s-" + uuid().slice(0, 12),
      session_start: now_ts(),
    };
    setParticipant(p);
    setPhase(2);
  };

  const handleProceedToTask = () => setPhase(3);
  const handleTaskComplete = (logs) => { setSessionLogs(logs); setPhase(4); };
  const handleReset = () => { setPhase(1); setParticipant(null); setSessionLogs([]); };

  return (
    <>
      <FontLoader />
      <style>{css}</style>
      <div className="app">
        <TopBar participant={participant} phase={phase} />
        <div className="main">
          {phase === 1 && <PhaseOnboard onStart={handleStart} />}
          {phase === 2 && <PhaseCondition participant={participant} onContinue={handleProceedToTask} />}
          {phase === 3 && <PhaseTask participant={participant} onComplete={handleTaskComplete} />}
          {phase === 4 && <PhaseResults participant={participant} logs={sessionLogs} onReset={handleReset} />}
        </div>
      </div>
    </>
  );
}
