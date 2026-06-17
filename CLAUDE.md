# CLAUDE.md — javierdearcos.com

Personal website. **Buildless static site** — no framework, no bundler, no
package.json. Native Web Components + ES modules + component-scoped CSS.
Deployed via GitHub Pages on the apex domain `javierdearcos.com`.

## Run

ES modules and `data/` imports need HTTP (won't work from `file://`):

```bash
python3 -m http.server 8000   # open http://localhost:8000
```

There is no build or test step. To "deploy", commit to the default branch —
GitHub Pages serves the repo as-is.

## Architecture

- **Web Components in light DOM** (no Shadow DOM) so the global stylesheet and
  the i18n pass apply normally. Defined in `js/components/` (`<talk-card>`,
  `<collab-card>`, `<post-card>`, `<focus-card>`, `<project-card>`).
- **Content lives in `data/*.js`** as plain arrays. Edit the array to update the
  site — no markup changes. `js/render.js`'s `renderCards()` creates one element
  per item, assigns it to the element's `.data` property, and appends it to a
  mount point in the HTML.
- **CSS** is one file per UI area, imported in order by `css/main.css`
  (`tokens → base → layout → components`). `css/blog.css` adds article typography
  for `/blog/` and the listing subpages.
- **i18n** (`js/i18n.js`): translatable nodes carry `data-i18n="key"` and
  `applyLang()` rewrites them from the catalog. For prose that ships in both
  languages at once (blog posts), use sibling `data-lang="es|en"` blocks instead —
  `applyLang()` shows the active one and hides the other. The chosen language is
  persisted in `localStorage` (`lang`) and carries across pages. Default is **ES**.

## Conventions & gotchas

- **Render cards before the first `applyLang()`** — cards emit `data-i18n`
  labels, so they must exist when the i18n pass runs (see `init` in `js/main.js`).
- **Home previews only the first N items** in a wrapping `.card-grid`, then a
  "see all" link to a subpage: `PREVIEW_COUNT = 4` (talks, collabs),
  `PROJECTS_PREVIEW = 3` (`js/main.js`). Subpages (`/talks/`, `/collabs/`,
  `/projects/`) render the full arrays via the same components + `renderCards()`
  into the same `.card-grid`. One data edit updates both.
- The element `.data` setter renders immediately, so a component must be
  defined/imported before `createElement`.
- Repo root holds source **and** year-numbered folders (`2020/`–`2025/`) that are
  **static redirect stubs** (`<meta http-equiv="refresh">` + `rel=canonical`) for
  old Hexo URLs (`/YYYY/MM/slug/` → `/blog/<slug>/`). Don't treat them as content.
- `CNAME` (apex domain) and `.nojekyll` (serve files as-is) must stay at the root.

## Subsystems

- **Blog** (`/blog/`): fully pre-rendered static HTML, one folder per post.
  Content source of truth is `blog-src/<slug>/` (`meta.json` + `es.html` + `en.html`);
  regenerate the whole blog (pages, listing, redirect stubs) with
  `tools/build-blog.py` — don't hand-edit generated pages. Each page ships **both
  languages inline**: every language-specific node is a `data-lang="es|en"` block
  and `applyLang()` (js/i18n.js) shows the active one; UI chrome uses `data-i18n`.
  An empty `en.html` falls back to the Spanish body with an "untranslated" notice.
  `tools/migrate-blog.py` is the legacy one-time Hexo importer (now superseded; it
  fetched the live Hexo URLs that are now redirect stubs). `tools/extract-blog-src.py`
  is the one-time bootstrap that built `blog-src/` from the already-generated pages.
  Featured posts are curated in `data/posts.js` (bilingual `{es,en}` fields),
  linking to `/blog/<slug>/`.
- **Contact** (`/contact/`): no backend; form posts to Formspree (id already set
  in the form `action`). `js/contact.js` submits via `fetch` with inline status;
  falls back to a plain POST without JS. `_gotcha` honeypot filters bots.

## File map

```
index.html              Home: shell + static sections + mount points
talks/ collabs/         Full-list subpages (js/talks.js, js/collabs.js)
projects/ contact/      Full projects list / contact form
career/                 Career timeline subpage
blog/<slug>/            Pre-rendered post pages + images; /blog/ is the listing
blog-src/<slug>/        Blog content source: meta.json + es.html + en.html
css/                    main.css imports per-area stylesheets + blog.css
js/                     main.js (home), per-subpage entries, shared:
                        render.js nav.js i18n.js theme.js
                        components/  custom elements
data/                   talks collabs posts projects focus tech  (content arrays)
tools/build-blog.py     Regenerates the bilingual blog from blog-src/
tools/extract-blog-src.py  One-time bootstrap: blog/ pages -> blog-src/
tools/migrate-blog.py   Legacy one-time Hexo importer (superseded)
CNAME .nojekyll         GitHub Pages config
```
