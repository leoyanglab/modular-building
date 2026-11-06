import manifest from "./pdf-manifest.json";
import { respondWithPdf } from "./pdf-response.js";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const file = manifest[url.pathname];
    return file
      ? respondWithPdf(request, env, url, file)
      : env.ASSETS.fetch(request);
  },
};
