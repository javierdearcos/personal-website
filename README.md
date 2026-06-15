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
css/
  main.css              Imports every layer below, in order
  tokens.css            Design tokens (colors, fonts) + light theme overrides
  base.css              Reset, base elements, skip link
  layout.css            Container + section headings
  buttons.css           .btn variants
  nav.css hero.css …    One stylesheet per UI area / component
js/
  main.js               Entry point: renders data → components, wires controls
  i18n.js               Translation catalog + language toggle
  theme.js              Dark/light theme + persistence
  carousel.js           Carousel scroll controls
  components/           Custom elements (<talk-card>, <project-card>, …)
data/
  talks.js collabs.js   Content as plain data arrays — edit these to update
  posts.js projects.js  the site without touching markup
  focus.js tech.js
```

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
