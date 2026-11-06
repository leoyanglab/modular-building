import { escapeHtml, normalize } from "./js/text.js";
import { createProductDialog } from "./js/product-dialog.js";
import { bindProjectBrief } from "./js/project-brief.js";

const grid = document.querySelector("#products"),
  series = document.querySelector("#series"),
  search = document.querySelector("#search"),
  more = document.querySelector("#load-more");
let products = [],
  filter = "all",
  limit = 12;
const openProduct = createProductDialog();
bindProjectBrief(() => products);

fetch("/products.json")
  .then((r) => {
    if (!r.ok) throw Error("catalog");
    return r.json();
  })
  .then((data) => {
    products = data;
    for (const c of [...new Set(products.map((p) => p.category))])
      series.add(
        new Option(
          c + " (" + products.filter((p) => p.category === c).length + ")",
          c,
        ),
      );
    const select = document.querySelector("[name=model]");
    select.replaceChildren(new Option("Još nisam odlučio/la", ""));
    for (const p of products)
      select.add(new Option((p.code || p.id) + " / " + p.name, p.id));
    render();
  })
  .catch(() => {
    grid.innerHTML =
      '<p>Kolekcija trenutno nije dostupna. <a href="/downloads/katalog-digital.pdf">Preuzmite PDF katalog.</a></p>';
  });
function reset() {
  limit = 12;
  render();
}
function render() {
  const q = normalize(search.value.trim()),
    matches = products.filter(
      (p) =>
        (filter === "all" || p.category === filter) &&
        (series.value === "all" || p.category === series.value) &&
        normalize(
          p.name +
            " " +
            p.category +
            " " +
            (p.code || "") +
            " " +
            (p.aliases || []).join(" ") +
            " " +
            (p.supplier || ""),
        ).includes(q),
    );
  grid.replaceChildren();
  for (const p of matches.slice(0, limit)) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "product-card";
    card.setAttribute("aria-label", `Pogledaj ${p.name}, ${p.area}`);
    card.innerHTML = `<img src="/images/${p.id}.webp" alt="${escapeHtml(p.name)}, prikaz proizvođača" width="900" height="600" loading="lazy"><small>${escapeHtml(p.code || p.id)} / ${escapeHtml(p.category)}</small><div class="card-title"><h3>${escapeHtml(p.name)}</h3><span>${escapeHtml(p.area)} &nbsp; ↗</span></div><p class="area-label">${escapeHtml(p.areaLabel)}</p><p>${escapeHtml(p.description)}</p>`;
    card.onclick = () => openProduct(p);
    grid.append(card);
  }
  document.querySelector("#result-count").textContent =
    `Prikazano ${Math.min(limit, matches.length)} od ${matches.length} modela · Ukupno ${products.length}`;
  if (!matches.length)
    grid.innerHTML =
      "<p>Nema modela za izabrane uslove. Promenite seriju ili pretragu.</p>";
  more.hidden = limit >= matches.length;
}
document.querySelectorAll("[data-filter]").forEach(
  (b) =>
    (b.onclick = () => {
      filter = b.dataset.filter;
      series.value = "all";
      document
        .querySelectorAll("[data-filter]")
        .forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      reset();
    }),
);
series.onchange = () => {
  filter = "all";
  document
    .querySelectorAll("[data-filter]")
    .forEach((x) =>
      x.setAttribute("aria-pressed", String(x.dataset.filter === "all")),
    );
  reset();
};
search.addEventListener("input", reset);
more.onclick = () => {
  limit += 12;
  render();
};
document.querySelector("#show-all").onclick = () => {
  limit = products.length;
  render();
};
document.querySelectorAll("[data-series]").forEach(
  (a) =>
    (a.onclick = () => {
      series.value = a.dataset.series;
      search.value = "";
      series.onchange();
    }),
);
