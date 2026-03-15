const recommendedOption = "Option A";
const recommendationId = "rec-001";
const participantStorageKey = "issr_task3_participant_id";
const statusLine = document.getElementById("status-line");
const taskPanel = document.getElementById("task-panel");

function randomParticipantId() {
  const alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let out = "P-";
  for (let i = 0; i < 8; i += 1) {
    out += alphabet[Math.floor(Math.random() * alphabet.length)];
  }
  return out;
}

function getParticipantId() {
  const params = new URLSearchParams(window.location.search);
  const queryParticipant = params.get("participant_id");
  if (queryParticipant) {
    localStorage.setItem(participantStorageKey, queryParticipant);
    return queryParticipant;
  }
  const existing = localStorage.getItem(participantStorageKey);
  if (existing) {
    return existing;
  }
  const created = randomParticipantId();
  localStorage.setItem(participantStorageKey, created);
  return created;
}

function hashString(value) {
  let hash = 0;
  for (let i = 0; i < value.length; i += 1) {
    hash = (hash * 31 + value.charCodeAt(i)) >>> 0;
  }
  return hash;
}

function selectCondition(conditions, participantId) {
  const idx = hashString(participantId) % conditions.length;
  return conditions[idx];
}

function setStatus(message, isError = false) {
  statusLine.textContent = message;
  statusLine.dataset.state = isError ? "error" : "ok";
}

async function loadConditions() {
  const response = await fetch("/api/conditions");
  if (!response.ok) {
    throw new Error(`condition fetch failed: ${response.status}`);
  }
  return response.json();
}

async function logDecision(payload) {
  const response = await fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const result = await response.json();
  if (!response.ok || result.status !== "ok") {
    throw new Error(result.message || "log write failed");
  }
}

async function bootstrap() {
  try {
    const participantId = getParticipantId();
    const config = await loadConditions();
    const condition = selectCondition(config.conditions, participantId);

    document.getElementById("participant-pill").textContent = `participant ${participantId}`;
    document.getElementById("condition-pill").textContent = `condition ${condition.id}`;
    document.getElementById("agent-name").textContent = condition.assistant_name;
    document.getElementById("agent-tone").textContent = `${condition.assistant_tone} tone | ${condition.confidence_frame} confidence`;
    document.getElementById("headline").textContent = condition.headline;
    document.getElementById("message").textContent = condition.message;
    taskPanel.hidden = false;

    const recommendationShownAt = performance.now();
    const buttons = [
      { id: "accept-btn", decision: "accept", matches: "true" },
      { id: "reject-btn", decision: "reject", matches: "false" }
    ];

    buttons.forEach(({ id, decision, matches }) => {
      document.getElementById(id).addEventListener("click", async () => {
        const payload = {
          participant_id: participantId,
          condition_id: condition.id,
          assistant_name: condition.assistant_name,
          assistant_tone: condition.assistant_tone,
          confidence_frame: condition.confidence_frame,
          decision,
          decision_matches_recommendation: matches,
          recommendation_id: recommendationId,
          recommended_option: recommendedOption,
          timestamp: new Date().toISOString(),
          latency_ms: Math.round(performance.now() - recommendationShownAt)
        };

        try {
          await logDecision(payload);
          setStatus(`Decision recorded: ${decision}`);
        } catch (error) {
          setStatus(error.message, true);
        }
      });
    });
  } catch (error) {
    setStatus(error.message, true);
  }
}

bootstrap();
