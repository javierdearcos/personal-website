/**
 * Light/dark theme handling. The chosen theme is persisted in
 * localStorage and reflected on <html data-theme>, which the CSS
 * tokens key off.
 */
const STORAGE_KEY = 'theme';

/** Apply `theme` ('dark' | 'light') and persist it. */
export function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.getElementById('themeToggle');
  if (btn) {
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  }
  localStorage.setItem(STORAGE_KEY, theme);
}

/** Resolve the initial theme from storage, falling back to the OS preference. */
export function initTheme() {
  const saved = localStorage.getItem(STORAGE_KEY);
  const preferred = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  applyTheme(saved || preferred);
}

/** Wire the nav theme button to flip between dark and light. */
export function initThemeToggle() {
  const btn = document.getElementById('themeToggle');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });
}
