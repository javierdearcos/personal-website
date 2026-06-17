#!/usr/bin/env python3
"""Canonical blog generator. Reads per-language sources from blog-src/<slug>/
and renders the bilingual static blog under blog/.

Each post page embeds BOTH languages: every language-specific node is wrapped in
`data-lang="es"` / `data-lang="en"`, and js/i18n.js's applyLang() shows the active
one (same mechanism as the rest of the site). UI chrome uses `data-i18n` keys.

Source layout (see tools/extract-blog-src.py for the one-time bootstrap):
  blog-src/<slug>/meta.json   { dt, cat, img?, title{es,en}, desc{es,en}, read{es,en} }
  blog-src/<slug>/es.html     Spanish body fragment
  blog-src/<slug>/en.html     English body fragment (empty -> falls back to ES)

Outputs: blog/<slug>/index.html (posts), blog/index.html (listing),
old Hexo redirect stubs, CNAME and .nojekyll. Posts are ordered newest-first by dt.

Run:  python3 tools/build-blog.py
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
SRC = os.path.join(ROOT, "blog-src")
BASE = "https://javierdearcos.com"

MONTHS_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

CAT_EMOJI = {"personal": "🌱", "carrera profesional": "🚀",
             "liderazgo": "🧭", "desarrollo": "💻"}
CAT_SLUG = {"carrera profesional": "carrera", "desarrollo": "desarrollo",
            "liderazgo": "liderazgo", "personal": "personal"}
CAT_EN = {"personal": "personal", "carrera profesional": "career",
          "liderazgo": "leadership", "desarrollo": "development"}

# old Hexo path per slug, for the redirect stubs (/YYYY/MM/slug/ -> /blog/slug/)
HEXO_PATHS = {
    "tree-shaking": "2025/10/tree-shaking", "squid-game": "2025/07/squid-game",
    "the-window-is-open": "2025/06/the-window-is-open",
    "with-me-or-against-me": "2025/04/with-me-or-against-me", "i-am": "2024/12/i-am",
    "goodbye-songs": "2024/09/goodbye-songs", "pain-tolerance": "2024/03/pain-tolerance",
    "trg-23": "2023/10/trg-23", "the-swan": "2023/10/the-swan",
    "onboarding-the-other-side": "2023/02/onboarding-the-other-side",
    "2022": "2023/01/2022", "show-yourself": "2022/10/show-yourself",
    "onboardings": "2022/09/onboardings", "the-average-life": "2022/08/the-average-life",
    "dry": "2021/10/dry", "wonderland": "2021/06/wonderland",
    "pull-requests": "2021/03/pull-requests", "technical-tests": "2021/02/technical-tests",
    "2020": "2021/01/2020", "clean-code": "2020/07/clean-code",
    "hello-world": "2020/06/hello-world",
}


def esc(s):
    return html.escape(s, quote=True)


def fmt_date(iso):
    y, m, d = int(iso[0:4]), int(iso[5:7]), int(iso[8:10])
    return (f"{d} de {MONTHS_ES[m - 1]} de {y}",
            f"{MONTHS_EN[m - 1]} {d}, {y}",
            iso[0:10])


def lang_spans(es, en, esc_=True):
    """Two siblings, one per language; applyLang() shows the active one. The EN
    span starts hidden so the default (ES) render has no flash before JS runs."""
    e = esc(es) if esc_ else es
    n = esc(en) if esc_ else en
    return f'<span data-lang="es">{e}</span><span data-lang="en" hidden>{n}</span>'


# shared nav markup (bilingual, with language toggle) ------------------------
def nav(active):
    def link(href, key, label):
        cur = ' aria-current="page"' if active == href else ""
        return f'<li><a href="{href}"{cur} data-i18n="{key}">{label}</a></li>'
    links = "\n      ".join([
        link("/", "nav.home", "Inicio"),
        link("/career/", "nav.career", "Trayectoria"),
        link("/talks/", "nav.talks", "Charlas"),
        link("/collabs/", "nav.collabs", "Colaboraciones"),
        link("/projects/", "nav.projects", "Proyectos"),
        link("/blog/", "nav.blog", "Blog"),
        link("/contact/", "nav.contact", "Contacto"),
    ])
    return f'''  <nav class="nav" aria-label="Navegación principal">
    <a class="nav-logo" href="/">&gt;_ javierdearcos</a>
    <ul class="nav-links" id="navLinks" role="list">
      {links}
    </ul>
    <div class="nav-controls">
      <button class="btn-icon btn-lang" id="langToggle" type="button" aria-label="Switch language">EN</button>
      <button class="btn-icon" id="themeToggle" type="button" aria-label="Toggle theme">☀️</button>
      <button class="btn-icon nav-toggle" id="navToggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="navLinks">☰</button>
    </div>
  </nav>'''


FOOTER = f'''  <footer>
    <div class="container">
      <p>© 2026 Javier de Arcos · <a href="/" data-i18n="nav.home">Inicio</a> · <a href="/blog/" data-i18n="nav.blog">Blog</a></p>
    </div>
  </footer>'''


# ── load sources ─────────────────────────────────────────────────────
def load():
    items = []
    for slug in os.listdir(SRC):
        d = os.path.join(SRC, slug)
        mp = os.path.join(d, "meta.json")
        if not os.path.isfile(mp):
            continue
        meta = json.load(open(mp, encoding="utf-8"))
        es_body = open(os.path.join(d, "es.html"), encoding="utf-8").read().strip()
        en_path = os.path.join(d, "en.html")
        en_body = open(en_path, encoding="utf-8").read().strip() if os.path.exists(en_path) else ""
        items.append({"slug": slug, **meta, "es_body": es_body, "en_body": en_body})
    items.sort(key=lambda it: it["dt"], reverse=True)  # newest first
    return items


# ── per-post page ────────────────────────────────────────────────────
def post_page(it, older, newer):
    es_date, en_date, iso = fmt_date(it["dt"])
    cat = it["cat"]
    emoji = CAT_EMOJI[cat]
    og_img = f"{BASE}/blog/{it['slug']}/{it['img']}" if it.get("img") else ""

    # EN body: fall back to the Spanish original with a notice when untranslated.
    if it["en_body"]:
        en_body = it["en_body"]
    else:
        en_body = ('<p class="post-untranslated" data-i18n="blog.untranslated">This post '
                   'has not been translated to English yet. Showing the original Spanish '
                   'version.</p>\n' + it["es_body"])

    def pager(other, dir_key, dir_es, dir_en, cls):
        if not other:
            return "<span></span>"
        ttl = lang_spans(other["title"]["es"], other["title"]["en"])
        return (f'<a class="pager-link {cls}" href="/blog/{other["slug"]}/">'
                f'<span class="pager-dir" data-i18n="{dir_key}">{dir_es}</span>'
                f'<span class="pager-ttl">{ttl}</span></a>')

    pager_newer = pager(newer, "blog.newer", "← Más reciente", "← Newer", "pager-next")
    pager_older = pager(older, "blog.older", "Más antiguo →", "Older →", "pager-prev")

    return f'''<!DOCTYPE html>
<html lang="es" data-theme="dark" data-title-es="{esc(it["title"]["es"])} — Javier de Arcos" data-title-en="{esc(it["title"]["en"])} — Javier de Arcos">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(it["title"]["es"])} — Javier de Arcos</title>
  <meta name="description" content="{esc(it["desc"]["es"])}" />
  <meta name="author" content="Javier de Arcos" />
  <meta property="og:title" content="{esc(it["title"]["es"])}" />
  <meta property="og:description" content="{esc(it["desc"]["es"])}" />
  <meta property="og:type" content="article" />
  <meta property="og:image" content="{og_img}" />
  <meta property="article:published_time" content="{it["dt"]}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="canonical" href="{BASE}/blog/{it["slug"]}/" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/main.css" />
  <link rel="stylesheet" href="/css/blog.css" />
  <script type="module" src="/js/blog.js"></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": {json.dumps(it["title"]["es"], ensure_ascii=False)},
    "description": {json.dumps(it["desc"]["es"], ensure_ascii=False)},
    "datePublished": "{it["dt"]}",
    "author": {{ "@type": "Person", "name": "Javier de Arcos", "url": "{BASE}" }},
    "url": "{BASE}/blog/{it["slug"]}/"
  }}
  </script>
</head>
<body>
  <a href="#main" class="skip-link" data-i18n="skip">Saltar al contenido</a>

{nav("/blog/")}

  <main id="main">
    <div class="container">
      <article class="post">
        <header class="post-header">
          <a class="post-back" href="/blog/" data-i18n="blog.back">← Todos los posts</a>
          <div class="post-meta">
            <span class="tag">{emoji} {lang_spans(cat, CAT_EN[cat])}</span>
            <time datetime="{iso}">{lang_spans(es_date, en_date)}</time>
            <span class="post-read">· {lang_spans(it["read"]["es"], it["read"]["en"])} <span data-i18n="blog.readSuffix">de lectura</span></span>
          </div>
          <h1 class="post-title-full">{lang_spans(it["title"]["es"], it["title"]["en"])}</h1>
        </header>
        <div class="post-body" data-lang="es">
{it["es_body"]}
        </div>
        <div class="post-body" data-lang="en" hidden>
{en_body}
        </div>
      </article>

      <nav class="post-pager" aria-label="Más posts">
        {pager_newer}
        {pager_older}
      </nav>
    </div>
  </main>

{FOOTER}
</body>
</html>
'''


# ── listing page ─────────────────────────────────────────────────────
def index_page(items):
    rows = []
    for it in items:
        es_date, en_date, iso = fmt_date(it["dt"])
        cat = it["cat"]
        emoji = CAT_EMOJI[cat]
        rows.append(f'''        <li class="post-entry" data-cat="{CAT_SLUG[cat]}">
          <a class="post-entry-link" href="/blog/{it["slug"]}/">
            <div class="post-entry-meta">
              <span class="tag">{emoji} {lang_spans(cat, CAT_EN[cat])}</span>
              <time datetime="{iso}">{lang_spans(es_date, en_date)}</time>
              <span class="post-read">· {lang_spans(it["read"]["es"], it["read"]["en"])}</span>
            </div>
            <h2 class="post-entry-title">{lang_spans(it["title"]["es"], it["title"]["en"])}</h2>
            <p class="post-entry-desc">{lang_spans(it["desc"]["es"], it["desc"]["en"])}</p>
          </a>
        </li>''')
    rows_html = "\n".join(rows)

    cats = sorted({it["cat"] for it in items}, key=lambda c: list(CAT_EMOJI).index(c))
    filters = ['<button class="blog-filter is-active" data-filter="all" type="button" data-i18n="blog.filter.all">Todo</button>']
    for c in cats:
        filters.append(f'<button class="blog-filter" data-filter="{CAT_SLUG[c]}" type="button">{CAT_EMOJI[c]} {lang_spans(c, CAT_EN[c])}</button>')
    filters_html = "\n        ".join(filters)

    return f'''<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog — Javier de Arcos</title>
  <meta name="description" content="Artículos sobre ingeniería, liderazgo, cultura de equipo y carrera profesional, por Javier de Arcos." />
  <meta name="author" content="Javier de Arcos" />
  <meta property="og:title" content="Blog — Javier de Arcos" />
  <meta property="og:description" content="Artículos sobre ingeniería, liderazgo, cultura de equipo y carrera profesional." />
  <meta property="og:type" content="website" />
  <link rel="canonical" href="{BASE}/blog/" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/main.css" />
  <link rel="stylesheet" href="/css/blog.css" />
  <script type="module" src="/js/blog.js"></script>
</head>
<body>
  <a href="#main" class="skip-link" data-i18n="skip">Saltar al contenido</a>

{nav("/blog/")}

  <main id="main">
    <div class="container">
      <header class="blog-head">
        <p class="section-label" data-i18n="blog.index.label">Escritos</p>
        <h1 class="blog-title" data-i18n="blog.index.title">Blog</h1>
        <p class="blog-intro" data-i18n="blog.index.intro">Pienso escribiendo. Aquí comparto reflexiones sobre ingeniería, liderazgo, cultura de equipo y carrera profesional.</p>
      </header>

      <div class="blog-filters" role="group" aria-label="Filtrar por categoría">
        {filters_html}
      </div>

      <ul class="post-list" id="postList" role="list">
{rows_html}
      </ul>
    </div>
  </main>

{FOOTER}
</body>
</html>
'''


# ── redirect stubs for old Hexo URLs ─────────────────────────────────
STUB = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<title>Redirigiendo…</title>
<link rel="canonical" href="{base}/blog/{slug}/" />
<meta http-equiv="refresh" content="0; url=/blog/{slug}/" />
<meta name="robots" content="noindex" />
</head>
<body>
<p>Este post se ha movido. Redirigiendo a <a href="/blog/{slug}/">/blog/{slug}/</a>…</p>
<script>location.replace("/blog/{slug}/");</script>
</body>
</html>
'''


# ── write everything ─────────────────────────────────────────────────
items = load()
for i, it in enumerate(items):
    newer = items[i - 1] if i > 0 else None
    older = items[i + 1] if i < len(items) - 1 else None
    pdir = os.path.join(BLOG, it["slug"])
    os.makedirs(pdir, exist_ok=True)
    with open(os.path.join(pdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(post_page(it, older=older, newer=newer))

with open(os.path.join(BLOG, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_page(items))

n_en = sum(1 for it in items if it["en_body"])
print(f"Wrote {len(items)} post pages + index ({n_en} translated to EN).")

for slug, hexo in HEXO_PATHS.items():
    d = os.path.join(ROOT, hexo)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(STUB.format(base=BASE, slug=slug))
with open(os.path.join(ROOT, "CNAME"), "w") as f:
    f.write("javierdearcos.com\n")
open(os.path.join(ROOT, ".nojekyll"), "w").close()
print(f"Wrote {len(HEXO_PATHS)} redirect stubs + CNAME + .nojekyll")
