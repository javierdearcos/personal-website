/**
 * Application entry point.
 *
 * 1. Registers the custom elements (side-effect imports).
 * 2. Renders the data-driven sections into their containers.
 * 3. Wires up theme, language and carousel controls.
 *
 * Order matters: cards are rendered *before* applyLang() so the i18n pass
 * also reaches the data-i18n attributes the cards emit.
 */
import './components/talk-card.js';
import './components/collab-card.js';
import './components/post-card.js';
import './components/focus-card.js';
import './components/project-card.js';

import { talks } from '../data/talks.js';
import { collabs } from '../data/collabs.js';
import { posts } from '../data/posts.js';
import { focusAreas } from '../data/focus.js';
import { projects } from '../data/projects.js';
import { technologies } from '../data/tech.js';

import { applyLang, initLangToggle } from './i18n.js';
import { initTheme, initThemeToggle } from './theme.js';
import { initCarousels } from './carousel.js';

/** Create `tag` elements from `items`, assign `.data`, and append to `mountId`. */
function renderCards(mountId, tag, items) {
  const mount = document.getElementById(mountId);
  if (!mount) return;
  const frag = document.createDocumentFragment();
  for (const item of items) {
    const el = document.createElement(tag);
    el.data = item;
    frag.appendChild(el);
  }
  mount.appendChild(frag);
}

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
  renderCards('talksCarousel', 'talk-card', talks);
  renderCards('collabCarousel', 'collab-card', collabs);
  renderCards('postsCarousel', 'post-card', posts);
  renderCards('projectList', 'project-card', projects);
  renderTech('techGrid', technologies);
}

function init() {
  render();

  // Theme + language first paint.
  initTheme();
  applyLang('es');

  // Controls.
  initThemeToggle();
  initLangToggle();
  initCarousels();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
