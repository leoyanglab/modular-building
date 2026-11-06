export const escapeHtml = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
export const normalize = (s) =>
  s
    .toLocaleLowerCase("sr-Latn")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
