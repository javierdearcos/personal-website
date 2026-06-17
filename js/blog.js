/**
 * Blog pages entry point.
 *
 * Reuses the global theme handling (shared localStorage key, so the
 * choice carries over from the home page) and wires the category
 * filter on the listing page. No i18n: posts are authored in Spanish.
 */
import { initTheme, initThemeToggle } from './theme.js';
import { initNav } from './nav.js';

/** Wire the category filter buttons on the blog index, if present. */
function initFilters() {
  const buttons = document.querySelectorAll('.blog-filter');
  const entries = document.querySelectorAll('.post-entry');
  if (!buttons.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      buttons.forEach((b) => b.classList.toggle('is-active', b === btn));
      entries.forEach((entry) => {
        const show = filter === 'all' || entry.dataset.cat === filter;
        entry.hidden = !show;
      });
    });
  });
}

function init() {
  initTheme();
  initThemeToggle();
  initNav();
  initFilters();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
