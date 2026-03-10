import express from "express";
import crypto from "crypto";
import { qualityForEvent, summarizeSessions, toCsv, validateEvent } from "./lib/event-core.js";

export function createApp(store, opts = {}) {
  const app = express();
  app.use(express.json({ limit: "256kb" }));

  app.get("/api/health", (_req, res) => {
    res.json({ ok: true, service: "trustlab-logger" });
  });

  app.post("/api/log-event", async (req, res) => {
    const body = req.body ?? {};
    const validationErr = validateEvent(body);
    if (validationErr) {
      res.status(400).json({ ok: false, error: validationErr });
      return;
    }

    const server_timestamp = new Date().toISOString();
    const event_id = crypto.randomUUID();
    const quality = qualityForEvent(body);
    const event = { ...body, ...quality, event_id, server_timestamp };

    try {
      await store.appendEvent(event);
      res.status(201).json({ ok: true, event_id, server_timestamp, quality_score: quality.quality_score });
    } catch (err) {
      res.status(500).json({ ok: false, error: "write_failed", detail: String(err) });
    }
  });

  app.get("/api/events.json", async (_req, res) => {
    try {
      const events = await store.readEvents();
      res.json({ count: events.length, events });
    } catch (err) {
      res.status(500).json({ ok: false, error: "read_failed", detail: String(err) });
    }
  });

  app.get("/api/events.csv", async (_req, res) => {
    try {
      const events = await store.readEvents();
      const csv = toCsv(events);
      res.setHeader("Content-Type", "text/csv; charset=utf-8");
      res.setHeader("Content-Disposition", "attachment; filename=trustlab_events.csv");
      res.send(csv);
    } catch (err) {
      res.status(500).json({ ok: false, error: "read_failed", detail: String(err) });
    }
  });

  app.get("/api/quality-report.json", async (_req, res) => {
    try {
      const events = await store.readEvents();
      const sessions = summarizeSessions(events, { dropoutMinutes: opts.dropoutMinutes ?? 20 });
      res.json({ sessions_count: sessions.length, sessions });
    } catch (err) {
      res.status(500).json({ ok: false, error: "report_failed", detail: String(err) });
    }
  });

  return app;
}
