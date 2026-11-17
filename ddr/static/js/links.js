// Links of the buttons of the page. A button with an empty link stays greyed out.
// Fill in the values below when the resources are online.
const LINKS = {
  paper:   "https://arxiv.org/pdf/2605.23762",   // e.g. "https://arxiv.org/pdf/XXXX.XXXXX"
  arxiv:   "https://arxiv.org/abs/2605.23762",   // e.g. "https://arxiv.org/abs/XXXX.XXXXX"
  video:   "#video",
  code:    "",   // e.g. "https://github.com/<organization>/<repository>"
  dataset: "",   // e.g. "https://huggingface.co/datasets/<organization>/<dataset>"
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-link]").forEach((a) => {
    const url = LINKS[a.dataset.link];
    if (!url) { a.title = "Coming soon"; return; }
    a.href = url;
    if (/^https?:/.test(url)) { a.target = "_blank"; a.rel = "noopener"; }
  });
});
