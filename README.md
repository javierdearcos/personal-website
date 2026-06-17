# javierdearcos.com

Personal website — a static, buildless site using native **Web Components**, ES
modules, and component-scoped CSS. No framework, no bundler.

## Running locally

ES modules and the `data/` imports require HTTP (they won't work from `file://`).
Serve the folder with any static server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
index.html              Page shell + static sections; declares mount points
talks/
  index.html            Full talks listing (home shows 4)
collabs/
  index.html            Full collaborations listing (home shows 4)
projects/
  index.html            Full projects listing (home shows 3)
contact/
  index.html            Contact form (Formspree) + social links
css/
  main.css              Imports every layer below, in order
  tokens.css            Design tokens (colors, fonts) + light theme overrides
  base.css              Reset, base elements, skip link
  layout.css            Container + section headings
  buttons.css           .btn variants
  nav.css hero.css …    One stylesheet per UI area / component
  blog.css              Blog/subpage listing + article typography (/blog/, /talks/, …)
js/
  main.js               Entry point: renders data → components, wires controls
  talks.js              Talks subpage entry: renders the full talks grid
  collabs.js            Collaborations subpage entry: renders the full grid
  projects.js           Projects subpage entry: renders the full projects list
  contact.js            Contact subpage entry: theme/i18n + Formspree submit
  blog.js               Blog entry point: theme + listing category filter
  render.js             Shared renderCards() helper (home carousels + grids)
  nav.js                Shared mobile hamburger toggle (all pages)
  i18n.js               Translation catalog + language toggle
  theme.js              Dark/light theme + persistence
  carousel.js           Carousel scroll controls
  components/           Custom elements (<talk-card>, <project-card>, …)
data/
  talks.js collabs.js   Content as plain data arrays — edit these to update
  posts.js projects.js  the site without touching markup
  focus.js tech.js
blog/
  index.html            Post listing (all posts, with category filters)
  <slug>/index.html     One pre-rendered static page per post
  <slug>/<image>        Post images, served alongside the page
```

## Blog

The blog lives under `/blog/` as fully static, pre-rendered HTML — one folder
per post. Each post page links the shared `css/main.css` (tokens, nav, footer)
plus `css/blog.css` (article typography), and `js/blog.js` (theme toggle). The
posts were migrated from the previous Hexo site; the listing at `/blog/`
provides category filtering. Featured posts on the home page are curated in
`data/posts.js` and link to the corresponding `/blog/<slug>/` page.

The old Hexo URLs (`/YYYY/MM/slug/`) are preserved as static redirect stubs
(`<meta http-equiv="refresh">` + `rel=canonical`) pointing at the new
`/blog/<slug>/` pages, so existing links and search results keep working on
GitHub Pages (which has no server-side redirect rules). `CNAME` sets the apex
domain and `.nojekyll` tells Pages to serve files as-is.

`tools/migrate-blog.py` regenerates the whole blog (post pages, images,
listing, and redirect stubs) from the live source — re-run it if migrating
again.

## Talks & collaborations

The home page previews only the first four talks and collaborations in their
carousels (`CAROUSEL_PREVIEW` in `js/main.js`), each followed by a "see all"
link. The full lists live on separate subpages — talks at `/talks/`
(`js/talks.js` + `data/talks.js`) and collaborations at `/collabs/`
(`js/collabs.js` + `data/collabs.js`) — each reusing the same `<talk-card>` /
`<collab-card>` elements and the shared `renderCards()` helper, just laid out as
wrapping grids (`.card-grid`) instead of carousels. Adding an item to either
data array updates both the home preview and its subpage with no markup changes.

The same pattern applies to projects: the home page previews the first three
(`PROJECTS_PREVIEW` in `js/main.js`) followed by a "see all" link, and the full
list lives at `/projects/`, rendered from `data/projects.js` via the shared
`renderCards()` helper.

## Contact

`/contact/` hosts a contact form plus the same social links shown on the home
page. The site has no backend, so the form posts to [Formspree](https://formspree.io)
(the form id is configured in the `action` of the form in `contact/index.html`).
`js/contact.js` enhances it to submit via `fetch` and show an inline
status without leaving the page; with JS disabled it falls back to a normal
POST. A `_gotcha` honeypot field filters out bots.

## How it fits together

- **Content lives in `data/`.** To add a talk, post, project, etc., edit the
  matching array — no HTML changes needed.
- **`main.js`** instantiates a custom element per data item, assigns the item to
  its `.data` property, and appends it to the matching mount point in
  `index.html` (e.g. `#talksCarousel`).
- **Components render into light DOM** (no Shadow DOM), so the global stylesheet
  and the i18n pass apply to them normally.
- **i18n:** translatable nodes carry `data-i18n="key"`; `applyLang()` rewrites
  them from the catalog in `i18n.js`. Cards are rendered before the first
  `applyLang()` so their `data-i18n` labels get translated too.
