/**
 * ParticipantService — generates and persists a participant ID.
 */

const STORAGE_KEY = "trustlab_participant_id";
const ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const ID_LENGTH = 8;

/**
 * Generate a random participant ID of the form P-[A-Z0-9]{8}.
 * @returns {string}
 */
function generateId() {
  let out = "P-";
  for (let i = 0; i < ID_LENGTH; i++) {
    out += ALPHABET[Math.floor(Math.random() * ALPHABET.length)];
  }
  return out;
}

/**
 * Return the participant ID for this browser session.
 * Priority: query-string param → localStorage → newly generated.
 * @returns {string}
 */
export function getParticipantId() {
  const params = new URLSearchParams(window.location.search);
  const fromQuery = params.get("participant_id");
  if (fromQuery) {
    localStorage.setItem(STORAGE_KEY, fromQuery);
    return fromQuery;
  }
  const existing = localStorage.getItem(STORAGE_KEY);
  if (existing) {
    return existing;
  }
  const created = generateId();
  localStorage.setItem(STORAGE_KEY, created);
  return created;
}
