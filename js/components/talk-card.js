/**
 * <talk-card> — a single talk in the Talks grid.
 *
 * Usage (set the `data` property, not an attribute):
 *   const el = document.createElement('talk-card');
 *   el.data = { langTag, year, title, event, slides?, video? };
 *
 * Renders into light DOM so the global stylesheet and the i18n pass
 * (the Slides/Video labels carry data-i18n) keep working.
 */
class TalkCard extends HTMLElement {
  set data(value) {
    this._data = value;
    this.render();
  }

  connectedCallback() {
    if (this._data) this.render();
  }

  render() {
    const { langTag, year, icon, title, event, slides, video, audio, url } = this._data;
    const links = [
      slides && `<a href="${slides}" target="_blank" rel="noopener" class="link-pill">🖥️ <span data-i18n="link.slides">Slides</span></a>`,
      video && `<a href="${video}" target="_blank" rel="noopener" class="link-pill">🎬 <span data-i18n="link.video">Video</span></a>`,
      audio && `<a href="${audio}" target="_blank" rel="noopener" class="link-pill">🎧 <span data-i18n="link.audio">Audio</span></a>`,
      url && `<a href="${url}" target="_blank" rel="noopener" class="link-pill">🔗 <span data-i18n="link.url">URL</span></a>`,
    ].filter(Boolean).join('');

    const titleIcon = icon || (video ? '🎥' : audio ? '🎧' : url ? '🔗' : '');

    this.className = 'talk-card';
    this.setAttribute('role', 'listitem');
    this.innerHTML = `
      <div class="talk-meta">
        <span class="tag">${langTag}</span><span class="tag">${year}</span>
      </div>
      <h3 class="talk-title"><span class="talk-type" aria-hidden="true">${titleIcon} </span>${title}</h3>
      <p class="talk-event">${event}</p>
      <div class="talk-links">${links}</div>`;
  }
}

customElements.define('talk-card', TalkCard);
