const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");
const root = path.resolve(__dirname, "..");
const products = require("../public/products.json");
const manifest = require("../src/pdf-manifest.json");
assert.equal(products.length, 219);
assert.equal(new Set(products.map((p) => p.id)).size, products.length);
for (const [url, pdf] of Object.entries(manifest)) {
  const chunks = pdf.parts.map((part) => {
    const bytes = fs.readFileSync(path.join(root, "public", part.path));
    assert.equal(bytes.length, part.size, part.path);
    return bytes;
  });
  const bytes = Buffer.concat(chunks);
  assert.equal(bytes.length, pdf.size, url);
  assert.equal(
    crypto.createHash("sha256").update(bytes).digest("hex"),
    pdf.sha256,
    url,
  );
  assert.equal(bytes.subarray(0, 5).toString(), "%PDF-");
}
for (const file of [
  "src/worker.js",
  "src/pdf-response.js",
  "public/app.js",
  ...fs
    .readdirSync(path.join(root, "public/js"))
    .filter((name) => name.endsWith(".js"))
    .map((name) => "public/js/" + name),
]) {
  require("node:child_process").execFileSync(process.execPath, [
    "--check",
    path.join(root, file),
  ]);
}
console.log(
  "Verified 219 unique products, both PDF byte counts and SHA-256 hashes, JavaScript syntax.",
);
