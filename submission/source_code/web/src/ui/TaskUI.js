/**
 * TaskUI — renders the experimental task panel and wires up button handlers.
 */

/**
 * Set the status message below the task buttons.
 * @param {string} message
 * @param {boolean} isError
 */
export function setStatus(message, isError = false) {
  const el = document.getElementById("status-line");
  if (!el) return;
  el.textContent = message;
  el.dataset.state = isError ? "error" : "ok";
}

/**
 * Populate the task panel with condition and participant data.
 * @param {string} participantId
 * @param {object} condition
 */
export function renderTask(participantId, condition) {
  document.getElementById("participant-pill").textContent = `participant ${participantId}`;
  document.getElementById("condition-pill").textContent = `condition ${condition.id}`;
  document.getElementById("agent-name").textContent = condition.assistant_name;
  document.getElementById("agent-tone").textContent =
    `${condition.assistant_tone} tone | ${condition.confidence_frame} confidence`;
  document.getElementById("headline").textContent = condition.headline;
  document.getElementById("message").textContent = condition.message;
  document.getElementById("task-panel").hidden = false;
}

/**
 * Attach click handlers to Accept/Reject buttons.
 * @param {Function} onDecision - Called with (decision, latencyMs)
 */
export function bindButtons(onDecision) {
  const buttons = [
    { id: "accept-btn", decision: "accept" },
    { id: "reject-btn", decision: "reject" },
  ];
  buttons.forEach(({ id, decision }) => {
    const btn = document.getElementById(id);
    if (btn) {
      btn.addEventListener("click", () => onDecision(decision));
    }
  });
}
