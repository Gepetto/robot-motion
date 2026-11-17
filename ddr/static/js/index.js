// Carousels, autoplay of the visible videos, BibTeX copy.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-carousel]").forEach(initCarousel);

  const copy = document.getElementById("copy-bib");
  if (copy) {
    copy.addEventListener("click", async () => {
      const text = document.getElementById("bibtex-code").innerText;
      try { await navigator.clipboard.writeText(text); } catch (e) { return; }
      const label = copy.querySelector("span:last-child");
      label.textContent = "Copied";
      setTimeout(() => (label.textContent = "Copy"), 1500);
    });
  }

  // Videos of the grids (and the dataset video) play when they are on screen
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const v = e.target;
      if (e.isIntersecting) { v.preload = "auto"; v.play().catch(() => {}); } else { v.pause(); }
    });
  }, { threshold: 0.35 });
  document.querySelectorAll("video[data-autoplay]").forEach((v) => io.observe(v));
});

function initCarousel(root) {
  const track = root.querySelector(".carousel-track");
  const slides = [...track.children];
  const dots = root.querySelector(".carousel-dots");
  const prev = root.querySelector(".prev");
  const next = root.querySelector(".next");
  let current = 0;

  slides.forEach((_, i) => {
    const b = document.createElement("button");
    b.setAttribute("aria-label", `Slide ${i + 1}`);
    b.addEventListener("click", () => go(i));
    dots.appendChild(b);
  });

  function go(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: "smooth" });
  }
  function update() {
    const w = track.clientWidth;
    current = Math.round(track.scrollLeft / w);
    [...dots.children].forEach((d, i) => d.classList.toggle("on", i === current));
    prev.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    slides.forEach((s, i) => {
      const v = s.querySelector("video");
      if (!v) return;
      if (i === current) { v.preload = "auto"; v.play().catch(() => {}); } else { v.pause(); }
    });
  }
  prev.addEventListener("click", () => go(current - 1));
  next.addEventListener("click", () => go(current + 1));
  let timer;
  track.addEventListener("scroll", () => { clearTimeout(timer); timer = setTimeout(update, 80); });
  window.addEventListener("resize", update);

  // A carousel plays its video only when it is on screen
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const v = slides[current] && slides[current].querySelector("video");
      if (!v) return;
      if (e.isIntersecting) v.play().catch(() => {}); else v.pause();
    });
  }, { threshold: 0.3 });
  io.observe(root);
  update();
}
