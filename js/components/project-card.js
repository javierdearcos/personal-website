/**
 * <project-card> — a single entry in the Projects list.
 *
 *   el.data = { icon, name, url, period, descKey, desc };
 *
 * The description carries a data-i18n key so the language toggle updates it.
 */
class ProjectCard extends HTMLElement {
  set data(value) {
    this._data = value;
    this.render();
  }

  connectedCallback() {
    if (this._data) this.render();
  }

  render() {
    const { icon, name, url, period, descKey, desc } = this._data;

    this.className = 'project-card';
    this.innerHTML = `
      <div class="project-icon" aria-hidden="true">${icon}</div>
      <div class="project-content">
        <p class="project-name"><a href="${url}" target="_blank" rel="noopener">${name}</a></p>
        <p class="project-period">${period}</p>
        <p class="project-desc" data-i18n="${descKey}">${desc}</p>
      </div>`;
  }
}

customElements.define('project-card', ProjectCard);
