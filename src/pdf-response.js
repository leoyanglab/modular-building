export async function respondWithPdf(request, env, url, file) {
  if (!["GET", "HEAD"].includes(request.method))
    return new Response("Method not allowed", {
      status: 405,
      headers: { Allow: "GET, HEAD" },
    });
  const etag = '"' + file.sha256 + '"';
  const headers = new Headers({
    "Content-Type": "application/pdf",
    "Content-Disposition":
      'inline; filename="' + url.pathname.split("/").pop() + '"',
    "Accept-Ranges": "bytes",
    ETag: etag,
    "Cache-Control": "public, max-age=0, must-revalidate",
    "X-Content-Type-Options": "nosniff",
  });
  if (request.headers.get("If-None-Match") === etag)
    return new Response(null, { status: 304, headers });
  let start = 0,
    end = file.size - 1,
    status = 200;
  const range = request.headers.get("Range");
  if (
    range &&
    (!request.headers.has("If-Range") ||
      request.headers.get("If-Range") === etag)
  ) {
    const match = /^bytes=(\d*)-(\d*)$/.exec(range);
    if (!match || (!match[1] && !match[2]))
      return new Response(null, {
        status: 416,
        headers: { "Content-Range": "bytes */" + file.size },
      });
    if (!match[1]) {
      start = Math.max(0, file.size - Number(match[2]));
    } else {
      start = Number(match[1]);
      if (match[2]) end = Math.min(Number(match[2]), end);
    }
    if (
      !Number.isSafeInteger(start) ||
      !Number.isSafeInteger(end) ||
      start > end ||
      start >= file.size
    )
      return new Response(null, {
        status: 416,
        headers: { "Content-Range": "bytes */" + file.size },
      });
    status = 206;
    headers.set("Content-Range", `bytes ${start}-${end}/${file.size}`);
  }
  headers.set("Content-Length", String(end - start + 1));
  if (request.method === "HEAD") return new Response(null, { status, headers });
  let offset = 0;
  const segments = [];
  for (const part of file.parts) {
    const a = Math.max(start, offset),
      b = Math.min(end, offset + part.size - 1);
    if (a <= b) segments.push({ part, start: a - offset, end: b - offset });
    offset += part.size;
  }
  let next = 0;
  const body = new ReadableStream({
    async pull(controller) {
      try {
        if (next === segments.length) {
          controller.close();
          return;
        }
        const seg = segments[next++];
        const partUrl = new URL(seg.part.path, url);
        const res = await env.ASSETS.fetch(new Request(partUrl));
        if (!res.ok) throw new Error("PDF segment unavailable");
        const bytes = new Uint8Array(await res.arrayBuffer());
        if (bytes.byteLength !== seg.part.size)
          throw new Error("PDF segment incomplete");
        controller.enqueue(bytes.subarray(seg.start, seg.end + 1));
      } catch (e) {
        controller.error(e);
      }
    },
  });
  return new Response(body, { status, headers });
}
