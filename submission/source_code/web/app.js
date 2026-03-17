import { getParticipantId } from "./src/services/ParticipantService.js";
import { fetchAssignedCondition } from "./src/services/ConditionService.js";
import { logDecision, flushQueue } from "./src/services/TelemetryService.js";
import { renderTask, bindButtons, setStatus } from "./src/ui/TaskUI.js";
import { now, elapsed } from "./src/utils/timing.js";

const RECOMMENDED_OPTION = "Option A";
const RECOMMENDATION_ID = "rec-001";

async function bootstrap() {
  // Attempt to flush any previously queued events from failed sessions.
  flushQueue().catch(() => {});

  try {
    const participantId = getParticipantId();
    const condition = await fetchAssignedCondition(participantId);

    renderTask(participantId, condition);

    const shownAt = now();

    bindButtons(async (decision) => {
      const latencyMs = elapsed(shownAt);
      const matches = decision === "accept" ? "true" : "false";

      const payload = {
        participant_id: participantId,
        condition_id: condition.id,
        assistant_name: condition.assistant_name,
        assistant_tone: condition.assistant_tone,
        confidence_frame: condition.confidence_frame,
        decision,
        decision_matches_recommendation: matches,
        recommendation_id: RECOMMENDATION_ID,
        recommended_option: RECOMMENDED_OPTION,
        timestamp: new Date().toISOString(),
        latency_ms: latencyMs,
      };

      try {
        await logDecision(payload);
        setStatus(`Decision recorded: ${decision}`);
      } catch (err) {
        setStatus(err.message || "Failed to record decision — will retry.", true);
      }
    });
  } catch (err) {
    setStatus(err.message || "Initialisation failed.", true);
  }
}

bootstrap();
