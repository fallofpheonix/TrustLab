import fs from "fs/promises";
import path from "path";

export function createFileStore({ dataDir, fileName }) {
  const LOG_FILE = path.join(dataDir, fileName);

  async function ensureStorage() {
    await fs.mkdir(dataDir, { recursive: true });
    try {
      await fs.access(LOG_FILE);
    } catch {
      await fs.writeFile(LOG_FILE, "", "utf8");
    }
  }

  async function readEvents() {
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

  async function appendEvent(event) {
    await ensureStorage();
    await fs.appendFile(LOG_FILE, JSON.stringify(event) + "\n", "utf8");
  }

  return {
    ensureStorage,
    readEvents,
    appendEvent,
    logPath: LOG_FILE,
  };
}
