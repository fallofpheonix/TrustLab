import path from "path";
import { fileURLToPath } from "url";
import { createApp } from "./app.js";
import { createFileStore } from "./lib/file-store.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const store = createFileStore({
  dataDir: path.join(__dirname, "data"),
  fileName: "events.jsonl",
});

const app = createApp(store, { dropoutMinutes: 20 });

const port = Number(process.env.PORT || 8787);
store.ensureStorage().then(() => {
  app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`trustlab backend listening on http://127.0.0.1:${port}`);
  });
});
