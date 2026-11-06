const base = process.env.SITE_URL || "http://127.0.0.1:4174";
const {
  chromium,
} = require("/Users/leo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const fs = require("fs"),
  crypto = require("crypto");
const expected = require("../public/products.json"),
  manifest = require("../src/pdf-manifest.json");
const assert = (v, m) => {
  if (!v) throw Error(m);
};
(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath:
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
  });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(base);
  await page.locator(".product-card").first().waitFor();
  assert(
    (await page.locator(".product-card").count()) === 12,
    "initial pagination",
  );
  await page.locator("#show-all").click();
  assert(
    (await page.locator(".product-card").count()) === 219,
    "all 219 visible",
  );
  await page.locator("#search").fill("SC-52");
  assert(
    (await page.locator(".product-card").count()) === 1,
    "last duplex searchable",
  );
  await page.locator(".product-card").click();
  assert(
    (await page.locator(".model-code").textContent()) === "SC-52",
    "correct source code",
  );
  await page.getByRole("button", { name: "Pripremi opis projekta" }).click();
  assert(
    (await page.locator("[name=model]").inputValue()) === "sc-52",
    "new model selected",
  );
  await page.locator("#search").fill("ZX-31");
  assert(
    (await page.locator(".product-card").count()) === 1,
    "ZX missing model restored",
  );
  await page.locator("#search").fill("Shi Guang");
  assert(
    (await page.locator(".product-card").count()) === 3,
    "all Shi Guang sizes",
  );
  await page.locator("#search").fill("X7");
  assert((await page.locator(".product-card").count()) === 1, "merged X7");
  await page.locator("#search").fill("");
  await page.locator("#series").selectOption("Modularni objekti");
  await page.locator("#show-all").click();
  assert((await page.locator(".product-card").count()) === 52, "all 52 duplex");
  await page.locator("#series").selectOption("all");
  await page.locator("#search").fill("Linglong 8 · 1");
  await page.locator(".product-card").click();
  assert(
    (await page.locator(".detail-gallery img").count()) === 1,
    "interior gallery",
  );
  await page.locator(".plan summary").click();
  await page.locator(".plan img").evaluate((i) => i.decode());
  await page.keyboard.press("Escape");
  await page.locator("#search").fill("");
  await page.getByRole("button", { name: "Svi modeli", exact: true }).click();
  const remote = await (await page.request.get(base + "/products.json")).json();
  assert(
    JSON.stringify(remote) === JSON.stringify(expected),
    "published catalog matches source",
  );
  assert(new Set(remote.map((p) => p.id)).size === 219, "unique ids");
  assert(
    (await page.locator("[name=model] option").count()) === 220,
    "all inquiry options",
  );
  for (const [path, m] of Object.entries(manifest)) {
    const head = await page.request.head(base + path);
    assert(
      head.status() === 200 &&
        Number(head.headers()["content-length"]) === m.size,
      "PDF HEAD",
    );
    const local = fs.readFileSync("output/pdf/" + path.split("/").pop());
    for (const [start, end] of [
      [0, 31],
      [4194290, 4194320],
      [m.size - 32, m.size - 1],
    ]) {
      const r = await page.request.get(base + path, {
        headers: { Range: `bytes=${start}-${end}` },
        timeout: 90000,
      });
      assert(r.status() === 206, "range status");
      assert(
        (await r.body()).equals(local.subarray(start, end + 1)),
        "range bytes",
      );
    }
    const invalid = await page.request.get(base + path, {
      headers: { Range: "bytes=" + m.size + "-" },
      timeout: 90000,
    });
    assert(invalid.status() === 416, "invalid range");
    if (!process.env.RANGE_ONLY) {
      const r = await page.request.get(base + path, { timeout: 180000 });
      assert(
        crypto
          .createHash("sha256")
          .update(await r.body())
          .digest("hex") === m.sha256,
        "full PDF integrity",
      );
    }
  }
  console.log("PDF range/integrity tests passed");
  await page.evaluate(async () => {
    await Promise.all(
      [...document.images].map((i) => {
        i.loading = "eager";
        return i.decode();
      }),
    );
  });
  await page.screenshot({
    path: "tmp/pdfs/luxury-desktop.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.locator("#search").blur();
  await page.screenshot({ path: "tmp/pdfs/luxury-mobile.png", fullPage: true });
  assert(
    !(await page.evaluate(
      () => document.documentElement.scrollWidth > innerWidth,
    )),
    "mobile overflow",
  );
  assert(!errors.length, errors.join("\n"));
  console.log(
    "PASS: 219 models, all 52 duplex, all 3 Shi Guang sizes, aliases, source parity, gallery/plan, desktop/mobile and PDF streaming.",
  );
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
