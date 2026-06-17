/**
 * Career subpage entry point.
 *
 * Renders the professional timeline. Reuses the same render helper, theme,
 * nav and i18n catalog as the rest of the site.
 */
import './components/career-card.js';

import { career } from '../data/career.js';

import { renderCards } from './render.js';
import { applyLang, initLang, initLangToggle } from './i18n.js';
import { initTheme, initThemeToggle } from './theme.js';
import { initNav } from './nav.js';

function init() {
  // Cards first, so applyLang() also reaches their data-i18n text.
  renderCards('careerTimeline', 'career-card', career);

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
