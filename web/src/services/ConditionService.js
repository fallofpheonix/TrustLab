/**
 * ConditionService — fetches the server-assigned condition for a participant.
 */

import { getJSON } from "../api/client.js";

/**
 * Fetch the server-assigned condition for the given participant_id.
 * Uses the /api/assign endpoint so condition assignment is server-side (SHA256).
 * @param {string} participantId
 * @returns {Promise<object>} The assigned condition object.
 */
export async function fetchAssignedCondition(participantId) {
  const data = await getJSON(
    `/api/assign?participant_id=${encodeURIComponent(participantId)}`
  );
  return data.condition;
}

/**
 * Fetch all available conditions from /api/conditions.
 * @returns {Promise<object[]>}
 */
export async function fetchAllConditions() {
  const data = await getJSON("/api/conditions");
  return data.conditions;
}
