import { escapeHtml } from "./text.js";

export function createProductDialog() {
  const dialog = document.querySelector("#product-dialog");
  function openProduct(p) {
    let specs = [
      [p.areaLabel, p.area],
      ["Unutrašnja površina", p.interior],
      ["Projekciona površina", p.footprint],
      ["Dodatna terasa", p.terrace],
      ["Dimenzije (D × Š × V)", p.dimensions],
      ["Približna masa", p.weight],
    ].filter(([k, v], i) => v && (i === 0 || k !== p.areaLabel));
    document.querySelector("#dialog-content").innerHTML =
      `<img src="/images/${p.id}.webp" alt="${escapeHtml(p.name)}, prikaz proizvođača"><p class="eyebrow">${escapeHtml(p.category)}</p><h2>${escapeHtml(p.name)}</h2><p class="model-code">${escapeHtml(p.code || p.id)}</p><p>${escapeHtml(p.description)}</p><dl class="specs">${specs.map(([k, v]) => `<div><dt>${escapeHtml(k)}</dt><dd>${escapeHtml(v)}</dd></div>`).join("")}</dl>${p.note ? `<p class="data-note">${escapeHtml(p.note)}</p>` : ""}<div class="detail-gallery">${(p.gallery || []).map((g) => `<figure><img src="/images/${escapeHtml(g)}.webp" alt="Dodatni prikaz modela ${escapeHtml(p.name)}" loading="lazy"><figcaption>Detalji iz kataloga proizvođača</figcaption></figure>`).join("")}</div>${p.plan ? `<details class="plan"><summary>Raspored / prikaz proizvođača</summary><img src="/images/${escapeHtml(p.plan)}.webp" alt="Izvorni prikaz rasporeda ${escapeHtml(p.name)}" loading="lazy"></details>` : ""}<p class="fine">${escapeHtml(p.supplier || "Zhongxin")}. Podaci i prikazi iz kataloga proizvođača. Konačna konfiguracija, oprema, cena i isporuka potvrđuju se pojedinačno. Prikaz nije projekat izveden u Srbiji.</p><button class="button dark" id="choose-model">Pripremi opis projekta <span>↗</span></button>`;
    dialog.showModal();
    document.querySelector("#choose-model").onclick = () => {
      document.querySelector("[name=model]").value = p.id;
      dialog.close();
      document.querySelector("#projekat").scrollIntoView();
      document.querySelector("[name=location]").focus({ preventScroll: true });
    };
  }

  document.querySelector(".close").onclick = () => dialog.close();
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (
        e.clientX < r.left ||
        e.clientX > r.right ||
        e.clientY < r.top ||
        e.clientY > r.bottom
      )
        dialog.close();
    }
  });

  return openProduct;
}
