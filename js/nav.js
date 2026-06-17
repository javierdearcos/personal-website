/**
 * Mobile navigation — hamburger toggle.
 *
 * Shared by every page's entry point. The button is hidden on desktop via CSS;
 * on narrow viewports it shows/hides the nav links dropdown. The menu closes
 * when a link is followed so navigating within the same page feels natural.
 */
export function initNav() {
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  if (!toggle || !links) return;

  const setOpen = (open) => {
    links.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? '✕' : '☰';
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  };

  toggle.addEventListener('click', () => {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  links.addEventListener('click', (e) => {
    if (e.target.closest('a')) setOpen(false);
  });
}
