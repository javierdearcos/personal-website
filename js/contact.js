/**
 * Contact subpage entry point.
 *
 * Reuses the shared theme + i18n, and progressively enhances the contact
 * form: when JS is available it submits to Formspree via fetch and shows an
 * inline status, so the visitor stays on the page. With JS disabled the form
 * still posts normally and Formspree renders its own confirmation page.
 */
import { applyLang, initLang, initLangToggle, t } from './i18n.js';
import { initTheme, initThemeToggle } from './theme.js';
import { initNav } from './nav.js';

function setStatus(el, key, state) {
  el.textContent = t(key);
  if (state) el.dataset.state = state;
  else delete el.dataset.state;
}

function initContactForm() {
  const form = document.getElementById('contactForm');
  const status = document.getElementById('formStatus');
  if (!form || !status) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submit = form.querySelector('[type="submit"]');
    submit.disabled = true;
    setStatus(status, 'form.sending');

    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      });
      if (res.ok) {
        setStatus(status, 'form.success', 'success');
        form.reset();
      } else {
        setStatus(status, 'form.error', 'error');
      }
    } catch {
      setStatus(status, 'form.error', 'error');
    } finally {
      submit.disabled = false;
    }
  });
}

function init() {
  initTheme();
  applyLang(initLang());

  initThemeToggle();
  initLangToggle();
  initNav();
  initContactForm();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
