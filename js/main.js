/**
 * Application entry point.
 *
 * 1. Registers the custom elements (side-effect imports).
 * 2. Renders the data-driven sections into their containers.
 * 3. Wires up theme, language and navigation controls.
 *
 * Order matters: cards are rendered *before* applyLang() so the i18n pass
 * also reaches the data-i18n attributes the cards emit.
 */
import './components/talk-card.js';
import './components/focus-card.js';
import './components/project-card.js';

import { talks } from '../data/talks.js';
import { collabs } from '../data/collabs.js';
import { posts } from '../data/posts.js';
import { focusAreas } from '../data/focus.js';
import { projects } from '../data/projects.js';
import { technologies } from '../data/tech.js';

import { applyLang, initLang, initLangToggle } from './i18n.js';
import { initTheme, initThemeToggle } from './theme.js';
import { renderCards } from './render.js';
import { initNav } from './nav.js';

/** Home grids preview only the first few items; the rest live on /talks/, etc. */
const PREVIEW_COUNT = 3;

/** Home projects list previews only the first few; the rest live on /projects/. */
const PROJECTS_PREVIEW = 3;

/** Render the plain tech badge list (no custom element needed). */
function renderTech(mountId, items) {
  const mount = document.getElementById(mountId);
  if (!mount) return;
  const frag = document.createDocumentFragment();
  for (const name of items) {
    const span = document.createElement('span');
    span.className = 'tech-badge';
    span.setAttribute('role', 'listitem');
    span.textContent = name;
    frag.appendChild(span);
  }
  mount.appendChild(frag);
}

function render() {
  renderCards('focusGrid', 'focus-card', focusAreas);
  renderCards('talksGrid', 'talk-card', talks.slice(0, PREVIEW_COUNT));
  renderCards('collabGrid', 'talk-card', collabs.slice(0, PREVIEW_COUNT));
  renderCards('postsGrid', 'talk-card', posts.slice(0, PREVIEW_COUNT));
  renderCards('projectList', 'project-card', projects.slice(0, PROJECTS_PREVIEW));
  renderTech('techGrid', technologies);
}

function init() {
  render();

  // Theme + language first paint.
  initTheme();
  applyLang(initLang());

  // Controls.
  initThemeToggle();
  initLangToggle();
  initNav();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
