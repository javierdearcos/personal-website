/**
 * Shared rendering helper.
 *
 * Creates one `tag` custom element per item, assigns the item to its `.data`
 * property, and appends them all to the `mountId` container in a single
 * fragment. Used by both the home page previews and the full-list subpages,
 * which both lay the cards out in a `.card-grid`.
 */
export function renderCards(mountId, tag, items) {
  const mount = document.getElementById(mountId);
  if (!mount) return;
  const frag = document.createDocumentFragment();
  for (const item of items) {
    const el = document.createElement(tag);
    el.data = item;
    frag.appendChild(el);
  }
  mount.appendChild(frag);
}
