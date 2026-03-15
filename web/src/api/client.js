/**
 * Low-level API client with configurable timeout and retry logic.
 */

const DEFAULT_TIMEOUT_MS = 10000;
const DEFAULT_RETRIES = 3;
const RETRY_DELAY_MS = 1000;

/**
 * Fetch with timeout support.
 * @param {string} url
 * @param {RequestInit} options
 * @param {number} timeoutMs
 * @returns {Promise<Response>}
 */
async function fetchWithTimeout(url, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timerId = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timerId);
  }
}

/**
 * Fetch with automatic retry on transient network failures.
 * @param {string} url
 * @param {RequestInit} options
 * @param {number} retries
 * @param {number} timeoutMs
 * @returns {Promise<Response>}
 */
export async function fetchWithRetry(
  url,
  options = {},
  retries = DEFAULT_RETRIES,
  timeoutMs = DEFAULT_TIMEOUT_MS
) {
  let lastError;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const response = await fetchWithTimeout(url, options, timeoutMs);
      return response;
    } catch (err) {
      lastError = err;
      if (attempt < retries) {
        await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY_MS * (attempt + 1)));
      }
    }
  }
  throw lastError;
}

/**
 * GET JSON from url, with timeout and retry.
 * @param {string} url
 * @returns {Promise<any>}
 */
export async function getJSON(url) {
  const response = await fetchWithRetry(url);
  if (!response.ok) {
    throw new Error(`GET ${url} failed: ${response.status}`);
  }
  return response.json();
}

/**
 * POST JSON body to url, with timeout and retry.
 * @param {string} url
 * @param {object} body
 * @returns {Promise<any>}
 */
export async function postJSON(url, body) {
  const response = await fetchWithRetry(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const result = await response.json();
  if (!response.ok || result.status !== "ok") {
    throw new Error(result.message || `POST ${url} failed: ${response.status}`);
  }
  return result;
}
