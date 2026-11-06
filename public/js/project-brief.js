export function bindProjectBrief(getProducts) {
  document.querySelector("#brief-form").onsubmit = (e) => {
    e.preventDefault();
    const d = new FormData(e.target),
      p = getProducts().find((p) => p.id === d.get("model"));
    const text = `OPIS PROJEKTA\nModularni prostori\n\nModel: ${p ? p.name : "Još nisam odlučio/la"}\nReferenca: ${p ? p.id : "-"}\nLokacija: ${d.get("location")}\nBroj jedinica: ${d.get("quantity")}\n\nIdeja:\n${d.get("idea")}\n\nDokument je sačuvan lokalno. Upit nije poslat.\n`;
    const url = URL.createObjectURL(
      new Blob(["\ufeff", text], { type: "text/plain;charset=utf-8" }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = "opis-projekta.txt";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    document.querySelector("#form-status").textContent =
      "Opis projekta je preuzet. Sačuvajte ga za budući razgovor.";
  };
}
