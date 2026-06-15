/**
 * <post-card> — a featured blog post in the Posts carousel.
 *
 *   el.data = { icon, tag, title, url, desc };
 */
class PostCard extends HTMLElement {
  set data(value) {
    this._data = value;
    this.render();
  }

  connectedCallback() {
    if (this._data) this.render();
  }

  render() {
    const { icon, tag, title, url, desc } = this._data;

    this.className = 'post-card';
    this.setAttribute('role', 'listitem');
    this.innerHTML = `
      <div class="post-icon" aria-hidden="true">${icon}</div>
      <span class="tag">${tag}</span>
      <h3 class="post-title"><a href="${url}" target="_blank" rel="noopener">${title}</a></h3>
      <p class="post-desc">${desc}</p>`;
  }
}

customElements.define('post-card', PostCard);
