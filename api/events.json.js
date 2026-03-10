import { readEvents } from "./_file-store.js";

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.status(405).json({ ok: false, error: "method_not_allowed" });
    return;
  }
  try {
    const events = await readEvents();
    res.status(200).json({ count: events.length, events });
  } catch (err) {
    res.status(500).json({ ok: false, error: "read_failed", detail: String(err) });
  }
}
