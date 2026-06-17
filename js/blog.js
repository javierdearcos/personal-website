/**
 * Blog pages entry point.
 *
 * Reuses the global theme + language handling (shared localStorage keys, so
 * both choices carry over from the home page) and wires the category filter on
 * the listing page. Posts ship both languages inline (data-lang blocks) and
 * applyLang() toggles which one is visible — same mechanism as the rest of the
 * site.
 */
import { initTheme, initThemeToggle } from './theme.js';
import { applyLang, initLang, initLangToggle } from './i18n.js';
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
  applyLang(initLang());
  initThemeToggle();
  initLangToggle();
  initNav();
  initFilters();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
