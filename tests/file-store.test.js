import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { createFileStore } from "../backend/lib/file-store.js";

test("file store appends and reads events", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "trustlab-store-"));
  const store = createFileStore({ dataDir: dir, fileName: "events.jsonl" });

  await store.ensureStorage();
  await store.appendEvent({ a: 1 });
  await store.appendEvent({ b: 2 });

  const events = await store.readEvents();
  assert.equal(events.length, 2);
  assert.deepEqual(events[0], { a: 1 });
  assert.deepEqual(events[1], { b: 2 });
});

test("file store ignores malformed JSON lines", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "trustlab-store-"));
  const store = createFileStore({ dataDir: dir, fileName: "events.jsonl" });

  await store.ensureStorage();
  await fs.appendFile(store.logPath, "{bad-json}\n", "utf8");
  await store.appendEvent({ ok: true });

  const events = await store.readEvents();
  assert.equal(events.length, 1);
  assert.deepEqual(events[0], { ok: true });
});
