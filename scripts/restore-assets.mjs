import { readFile, writeFile, mkdir, rename } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL("../", import.meta.url));
const manifest = JSON.parse(
  await readFile(
    new URL("../assets/published-assets.json", import.meta.url),
    "utf8",
  ),
);
const base = process.env.ASSET_BASE_URL || manifest.baseUrl;
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
let next = 0,
  restored = 0;
await Promise.all(
  Array.from({ length: 6 }, async () => {
    while (next < manifest.files.length) {
      const entry = manifest.files[next++];
      if (!/^public\/(images|_pdf)\/[a-zA-Z0-9_.-]+$/.test(entry.path))
        throw Error(`Invalid resource path: ${entry.path}`);
      const dest = resolve(root, entry.path);
      try {
        if (hash(await readFile(dest)) === entry.sha256) continue;
      } catch {}
      let lastError;
      for (let attempt = 0; attempt < 3; attempt++) {
        try {
          const response = await fetch(
            new URL(
              entry.path.slice(7),
              base.endsWith("/") ? base : base + "/",
            ),
            {
              headers: { "User-Agent": "Mozilla/5.0 ModularCatalogBuild/1.0" },
              signal: AbortSignal.timeout(60000),
            },
          );
          if (!response.ok) throw Error(`HTTP ${response.status}`);
          const bytes = Buffer.from(await response.arrayBuffer());
          if (bytes.length !== entry.size || hash(bytes) !== entry.sha256)
            throw Error("Resource integrity mismatch");
          await mkdir(dirname(dest), { recursive: true });
          await writeFile(dest + ".download", bytes);
          await rename(dest + ".download", dest);
          restored++;
          lastError = null;
          break;
        } catch (error) {
          lastError = error;
        }
      }
      if (lastError)
        throw Error(`Cannot restore ${entry.path}: ${lastError.message}`);
    }
  }),
);
console.log(
  `Verified ${manifest.files.length} published resources; restored ${restored}.`,
);
