// Links of the buttons of the page. A button with an empty link stays greyed out.
const LINKS = {
  paper: "https://arxiv.org/pdf/2508.02194",
  arxiv: "https://arxiv.org/abs/2508.02194",
  video: "#video",
  code:  "https://github.com/Gepetto/BoltLocomotion",
  logs:  "",   // coming soon
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-link]").forEach((a) => {
    const url = LINKS[a.dataset.link];
    if (!url) { a.title = "Coming soon"; return; }
    a.href = url;
    if (/^https?:/.test(url)) { a.target = "_blank"; a.rel = "noopener"; }
  });
});
