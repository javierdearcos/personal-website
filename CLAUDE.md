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
- **i18n** (`js/i18n.js`): translatable nodes carry `data-i18n="key"`;
  `applyLang()` rewrites them from the catalog. Default language is **ES**.

## Conventions & gotchas

- **Render cards before the first `applyLang()`** — cards emit `data-i18n`
  labels, so they must exist when the i18n pass runs (see `init` in `js/main.js`).
- **Home previews only the first N items**, then a "see all" link to a subpage:
  `CAROUSEL_PREVIEW = 4` (talks, collabs), `PROJECTS_PREVIEW = 3` (`js/main.js`).
  Subpages (`/talks/`, `/collabs/`, `/projects/`) render the full arrays via the
  same components + `renderCards()`. One data edit updates both.
- The element `.data` setter renders immediately, so a component must be
  defined/imported before `createElement`.
- Repo root holds source **and** year-numbered folders (`2020/`–`2025/`) that are
  **static redirect stubs** (`<meta http-equiv="refresh">` + `rel=canonical`) for
  old Hexo URLs (`/YYYY/MM/slug/` → `/blog/<slug>/`). Don't treat them as content.
- `CNAME` (apex domain) and `.nojekyll` (serve files as-is) must stay at the root.

## Subsystems

- **Blog** (`/blog/`): fully pre-rendered static HTML, one folder per post,
  migrated from Hexo. Regenerate the whole blog (pages, images, listing, redirect
  stubs) with `tools/migrate-blog.py` — don't hand-edit generated pages. Featured
  posts are curated in `data/posts.js`, linking to `/blog/<slug>/`.
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
css/                    main.css imports per-area stylesheets + blog.css
js/                     main.js (home), per-subpage entries, shared:
                        render.js nav.js i18n.js theme.js carousel.js
                        components/  custom elements
data/                   talks collabs posts projects focus tech  (content arrays)
tools/migrate-blog.py   Regenerates the blog from the Hexo source
CNAME .nojekyll         GitHub Pages config
```
