/**
 * <post-card> — a featured blog post in the Posts grid.
 *
 *   el.data = { icon, tag, title, url, desc };
 *
 * `tag`, `title` and `desc` may each be a plain string or a
 * `{ es, en }` pair; pairs render as two `data-lang` spans so the
 * global language toggle (applyLang) switches them in place.
 */
class PostCard extends HTMLElement {
  set data(value) {
    this._data = value;
    this.render();
  }

  connectedCallback() {
    if (this._data) this.render();
  }

  /** A string passes through; a `{es,en}` pair becomes two language spans. */
  bilingual(value) {
    if (value && typeof value === 'object') {
      return `<span data-lang="es">${value.es}</span><span data-lang="en">${value.en}</span>`;
    }
    return value;
  }

  render() {
    const { icon, tag, year, title, url, desc } = this._data;

    const links = [
      url && `<a href="${url}" target="_blank" rel="noopener" class="link-pill">🔗 <span data-i18n="link.url">URL</span></a>`,
    ].filter(Boolean).join('');

    this.className = 'post-card';
    this.setAttribute('role', 'listitem');
    this.innerHTML = `
      <div class="post-meta">
        <span class="tag">${this.bilingual(tag)}</span><span class="tag">${year}</span>
      </div>
      <h3 class="post-title"><span class="post-icon" aria-hidden="true">${icon} </span>${this.bilingual(title)}</h3>
      <p class="post-desc">${this.bilingual(desc)}</p>
      <div class="post-links">${links}</div>`;
  }
}

customElements.define('post-card', PostCard);
