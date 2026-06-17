/**
 * Talks subpage entry point.
 *
 * Renders the full list of talks (the home page only previews the first few).
 * Reuses the same data, custom element, theme and i18n as the home page.
 */
import './components/talk-card.js';

import { talks } from '../data/talks.js';

import { renderCards } from './render.js';
import { applyLang, initLang, initLangToggle } from './i18n.js';
import { initTheme, initThemeToggle } from './theme.js';
import { initNav } from './nav.js';

function init() {
  // Cards first, so applyLang() also reaches their data-i18n labels.
  renderCards('talksGrid', 'talk-card', talks);

  initTheme();
  applyLang(initLang());

  initThemeToggle();
  initLangToggle();
  initNav();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
