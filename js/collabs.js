/**
 * Collaborations subpage entry point.
 *
 * Renders the full list of collaborations (the home page only previews the
 * first few). Reuses the same data, custom element, theme and i18n as the
 * home page.
 */
import './components/collab-card.js';

import { collabs } from '../data/collabs.js';

import { renderCards } from './render.js';
import { applyLang, initLangToggle } from './i18n.js';
import { initTheme, initThemeToggle } from './theme.js';
import { initNav } from './nav.js';

function init() {
  // Cards first, so applyLang() also reaches their data-i18n labels.
  renderCards('collabsGrid', 'collab-card', collabs);

  initTheme();
  applyLang('es');

  initThemeToggle();
  initLangToggle();
  initNav();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
