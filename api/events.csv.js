import { readEvents } from "./_file-store.js";
import { toCsv } from "../backend/lib/event-core.js";

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.status(405).json({ ok: false, error: "method_not_allowed" });
    return;
  }
  try {
    const events = await readEvents();
    const csv = toCsv(events);
    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.setHeader("Content-Disposition", "attachment; filename=trustlab_events.csv");
    res.status(200).send(csv);
  } catch (err) {
    res.status(500).json({ ok: false, error: "read_failed", detail: String(err) });
  }
}
