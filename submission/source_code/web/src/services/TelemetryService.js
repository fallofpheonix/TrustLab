/**
 * TelemetryService — submits decision events with an offline retry queue.
 */

import { postJSON } from "../api/client.js";

const QUEUE_KEY = "trustlab_event_queue";

/**
 * Load the pending retry queue from localStorage.
 * @returns {object[]}
 */
function loadQueue() {
  try {
    return JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
  } catch {
    return [];
  }
}

/**
 * Persist the retry queue to localStorage.
 * @param {object[]} queue
 */
function saveQueue(queue) {
  localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
}

/**
 * Attempt to flush all queued events that failed previously.
 */
export async function flushQueue() {
  const queue = loadQueue();
  if (!queue.length) return;
  const remaining = [];
  for (const payload of queue) {
    try {
      await postJSON("/api/events", payload);
    } catch {
      remaining.push(payload);
    }
  }
  saveQueue(remaining);
}

/**
 * Submit a decision event to /api/events.
 * If the request fails, the event is queued for retry on next load.
 * @param {object} payload
 * @returns {Promise<object>} Server response.
 */
export async function logDecision(payload) {
  try {
    const result = await postJSON("/api/events", payload);
    await flushQueue(); // Drain any previously-queued events on success.
    return result;
  } catch (err) {
    const queue = loadQueue();
    queue.push(payload);
    saveQueue(queue);
    throw err;
  }
}
