import fs from "fs/promises";
import path from "path";

const DATA_DIR = "/tmp/trustlab-data";
const LOG_FILE = path.join(DATA_DIR, "events.jsonl");

async function ensureStorage() {
  await fs.mkdir(DATA_DIR, { recursive: true });
  try {
    await fs.access(LOG_FILE);
  } catch {
    await fs.writeFile(LOG_FILE, "", "utf8");
  }
}

export async function readEvents() {
  await ensureStorage();
  const raw = await fs.readFile(LOG_FILE, "utf8");
  return raw
    .split("\n")
    .filter(Boolean)
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

export async function appendEvent(event) {
  await ensureStorage();
  await fs.appendFile(LOG_FILE, JSON.stringify(event) + "\n", "utf8");
}
