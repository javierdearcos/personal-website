/**
 * <focus-card> — a focus area in the "What I care about" grid.
 *
 *   el.data = { icon, titleKey, title, descKey, desc };
 *
 * The title/desc carry data-i18n keys so the language toggle updates them;
 * `title`/`desc` are the Spanish defaults shown before the i18n pass.
 */
class FocusCard extends HTMLElement {
  set data(value) {
    this._data = value;
    this.render();
  }

  connectedCallback() {
    if (this._data) this.render();
  }

  render() {
    const { icon, titleKey, title, descKey, desc } = this._data;

    this.className = 'focus-card';
    this.setAttribute('role', 'listitem');
    this.innerHTML = `
      <div class="focus-icon" aria-hidden="true">${icon}</div>
      <div class="focus-title" data-i18n="${titleKey}">${title}</div>
      <p class="focus-desc" data-i18n="${descKey}">${desc}</p>`;
  }
}

customElements.define('focus-card', FocusCard);
