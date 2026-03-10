import crypto from "crypto";
import { appendEvent } from "./_file-store.js";
import { qualityForEvent, validateEvent } from "../backend/lib/event-core.js";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ ok: false, error: "method_not_allowed" });
    return;
  }
  const body = req.body ?? {};
  const validationErr = validateEvent(body);
  if (validationErr) {
    res.status(400).json({ ok: false, error: validationErr });
    return;
  }

  const event_id = crypto.randomUUID();
  const server_timestamp = new Date().toISOString();
  const quality = qualityForEvent(body);
  const event = { ...body, ...quality, event_id, server_timestamp };

  try {
    await appendEvent(event);
    res.status(201).json({ ok: true, event_id, server_timestamp, quality_score: quality.quality_score });
  } catch (err) {
    res.status(500).json({ ok: false, error: "write_failed", detail: String(err) });
  }
}
