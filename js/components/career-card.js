/**
 * <career-card> — a single role in the Career timeline.
 *
 * Usage (set the `data` property, not an attribute):
 *   const el = document.createElement('career-card');
 *   el.data = { id, company, bullets };
 *
 * Renders into light DOM so the global stylesheet applies. All text carries
 * `data-i18n` keys (career.<id>.role/period/summary/bN) and is left empty —
 * applyLang() fills it in, so this card must render *before* applyLang() runs.
 */
class CareerCard extends HTMLElement {
  set data(value) {
    this._data = value;
    this.render();
  }

  connectedCallback() {
    if (this._data) this.render();
  }

  render() {
    const { id, company, bullets } = this._data;
    const items = Array.from(
      { length: bullets },
      (_, i) => `<li data-i18n="career.${id}.b${i + 1}"></li>`
    ).join('');
    const list = bullets ? `<ul class="career-bullets">${items}</ul>` : '';

    this.className = 'career-card';
    this.setAttribute('role', 'listitem');
    this.innerHTML = `
      <div class="career-marker" aria-hidden="true"></div>
      <div class="career-content">
        <p class="career-role" data-i18n="career.${id}.role"></p>
        <p class="career-company">${company} · <span data-i18n="career.${id}.period"></span></p>
        <p class="career-summary" data-i18n="career.${id}.summary"></p>
        ${list}
      </div>`;
  }
}

customElements.define('career-card', CareerCard);
