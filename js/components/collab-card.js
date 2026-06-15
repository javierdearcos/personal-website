/**
 * <collab-card> — a podcast/interview in the Collaborations carousel.
 *
 *   el.data = { icon, iconLabel, langTag, title, source, url? };
 *
 * When `url` is present the title is a link; otherwise it is plain text.
 */
class CollabCard extends HTMLElement {
  set data(value) {
    this._data = value;
    this.render();
  }

  connectedCallback() {
    if (this._data) this.render();
  }

  render() {
    const { icon, iconLabel, langTag, title, source, url } = this._data;
    const heading = url
      ? `<a href="${url}" target="_blank" rel="noopener">${title}</a>`
      : title;

    this.className = 'collab-card';
    this.setAttribute('role', 'listitem');
    this.innerHTML = `
      <div class="collab-type" aria-label="${iconLabel}">${icon}</div>
      <span class="tag">${langTag}</span>
      <h3 class="collab-title">${heading}</h3>
      <p class="collab-source">${source}</p>`;
  }
}

customElements.define('collab-card', CollabCard);
