/**
 * Horizontal carousels. Each nav button declares its target carousel and
 * direction via data attributes:
 *
 *   <button class="carousel-btn" data-carousel-target="talksCarousel" data-carousel-dir="-1">
 *
 * Clicking scrolls by one card width (measured from the first card).
 */
function scrollCarousel(id, dir) {
  const el = document.getElementById(id);
  if (!el) return;
  const card = el.querySelector('.talk-card, .collab-card, .post-card');
  const amount = card ? card.offsetWidth + 16 : 320;
  el.scrollBy({ left: dir * amount, behavior: 'smooth' });
}

/** Attach click handlers to every `[data-carousel-target]` button. */
export function initCarousels() {
  document.querySelectorAll('[data-carousel-target]').forEach((btn) => {
    btn.addEventListener('click', () => {
      scrollCarousel(btn.dataset.carouselTarget, Number(btn.dataset.carouselDir));
    });
  });
}
