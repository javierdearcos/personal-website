/**
 * Projects subpage entry point.
 *
 * Renders the full list of projects (the home page only previews the first
 * few). Reuses the same data, custom element, theme and i18n as the home page.
 */
import './components/project-card.js';

import { projects } from '../data/projects.js';

import { renderCards } from './render.js';
import { applyLang, initLangToggle } from './i18n.js';
import { initTheme, initThemeToggle } from './theme.js';
import { initNav } from './nav.js';

function init() {
  // Cards first, so applyLang() also reaches their data-i18n descriptions.
  renderCards('projectList', 'project-card', projects);

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
