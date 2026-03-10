import { readEvents } from "./_file-store.js";
import { summarizeSessions } from "../backend/lib/event-core.js";

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.status(405).json({ ok: false, error: "method_not_allowed" });
    return;
  }
  try {
    const events = await readEvents();
    const sessions = summarizeSessions(events, { dropoutMinutes: 20 });
    res.status(200).json({ sessions_count: sessions.length, sessions });
  } catch (err) {
    res.status(500).json({ ok: false, error: "report_failed", detail: String(err) });
  }
}
