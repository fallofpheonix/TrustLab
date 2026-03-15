/**
 * High-resolution timing utilities using performance.now().
 */

/**
 * Returns the current high-resolution timestamp in milliseconds.
 * @returns {number}
 */
export function now() {
  return performance.now();
}

/**
 * Returns elapsed milliseconds since a previous timestamp, rounded to integer.
 * @param {number} since - A timestamp from now()
 * @returns {number}
 */
export function elapsed(since) {
  return Math.round(performance.now() - since);
}
