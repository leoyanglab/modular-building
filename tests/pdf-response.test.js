import test from "node:test";
import assert from "node:assert/strict";
import { respondWithPdf } from "../src/pdf-response.js";

const file = {
  size: 10,
  sha256: "test-etag",
  parts: [
    { path: "/_pdf/a.bin", size: 4 },
    { path: "/_pdf/b.bin", size: 6 },
  ],
};
function harness({ headers = {}, method = "GET", incomplete = false } = {}) {
  const reads = [];
  const env = {
    ASSETS: {
      async fetch(request) {
        reads.push(new URL(request.url).pathname);
        return new Response(
          request.url.endsWith("a.bin")
            ? "0123"
            : incomplete
              ? "456"
              : "456789",
        );
      },
    },
  };
  const request = new Request("https://test.local/downloads/catalog.pdf", {
    method,
    headers,
  });
  return {
    reads,
    response: () => respondWithPdf(request, env, new URL(request.url), file),
  };
}

test("PDF body preserves part order and streams a range across part boundaries", async () => {
  const full = harness();
  const response = await full.response();
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("content-length"), "10");
  assert.equal(await response.text(), "0123456789");
  assert.deepEqual(full.reads, ["/_pdf/a.bin", "/_pdf/b.bin"]);

  const range = await harness({ headers: { Range: "bytes=2-6" } }).response();
  assert.equal(range.status, 206);
  assert.equal(range.headers.get("content-range"), "bytes 2-6/10");
  assert.equal(range.headers.get("content-length"), "5");
  assert.equal(await range.text(), "23456");
});

test("suffix, open-ended, invalid and If-Range requests keep HTTP behavior", async () => {
  for (const [range, body] of [
    ["bytes=-3", "789"],
    ["bytes=8-", "89"],
  ]) {
    const response = await harness({ headers: { Range: range } }).response();
    assert.equal(response.status, 206);
    assert.equal(await response.text(), body);
  }
  for (const range of ["bytes=10-", "bytes=7-2", "bytes=-", "bytes=0-1,3-4"]) {
    const h = harness({ headers: { Range: range } });
    const response = await h.response();
    assert.equal(response.status, 416);
    assert.equal(response.headers.get("content-range"), "bytes */10");
    assert.deepEqual(h.reads, []);
  }
  const response = await harness({
    headers: { Range: "bytes=2-6", "If-Range": '"old"' },
  }).response();
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "0123456789");
});

test("HEAD, cache hits and unsupported methods do not read asset parts", async () => {
  for (const [options, status] of [
    [{ method: "HEAD" }, 200],
    [{ method: "HEAD", headers: { Range: "bytes=2-6" } }, 206],
    [{ headers: { "If-None-Match": '"test-etag"' } }, 304],
    [{ method: "POST" }, 405],
  ]) {
    const h = harness(options);
    const response = await h.response();
    assert.equal(response.status, status);
    assert.equal(
      await response.text(),
      status === 405 ? "Method not allowed" : "",
    );
    assert.deepEqual(h.reads, []);
  }
});

test("an incomplete PDF part fails the stream instead of silently truncating it", async () => {
  const response = await harness({ incomplete: true }).response();
  await assert.rejects(response.text(), /PDF segment incomplete/);
});
