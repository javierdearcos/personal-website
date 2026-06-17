#!/usr/bin/env python3
"""Generate static blog pages from the live Hexo site, matching the new site style."""
import os, re, json, html, urllib.request

ROOT = "/Users/javier/Projects/personal-website"
BLOG = os.path.join(ROOT, "blog")
BASE = "https://javierdearcos.com"
UA = {"User-Agent": "Mozilla/5.0 (migration script)"}

POSTS = [
    ("2025/10/tree-shaking", "tree-shaking", "personal"),
    ("2025/07/squid-game", "squid-game", "carrera profesional"),
    ("2025/06/the-window-is-open", "the-window-is-open", "carrera profesional"),
    ("2025/04/with-me-or-against-me", "with-me-or-against-me", "liderazgo"),
    ("2024/12/i-am", "i-am", "personal"),
    ("2024/09/goodbye-songs", "goodbye-songs", "personal"),
    ("2024/03/pain-tolerance", "pain-tolerance", "personal"),
    ("2023/10/trg-23", "trg-23", "personal"),
    ("2023/10/the-swan", "the-swan", "carrera profesional"),
    ("2023/02/onboarding-the-other-side", "onboarding-the-other-side", "carrera profesional"),
    ("2023/01/2022", "2022", "personal"),
    ("2022/10/show-yourself", "show-yourself", "carrera profesional"),
    ("2022/09/onboardings", "onboardings", "carrera profesional"),
    ("2022/08/the-average-life", "the-average-life", "personal"),
    ("2021/10/dry", "dry", "desarrollo"),
    ("2021/06/wonderland", "wonderland", "carrera profesional"),
    ("2021/03/pull-requests", "pull-requests", "desarrollo"),
    ("2021/02/technical-tests", "technical-tests", "carrera profesional"),
    ("2021/01/2020", "2020", "personal"),
    ("2020/07/clean-code", "clean-code", "desarrollo"),
    ("2020/06/hello-world", "hello-world", "personal"),
]

MONTHS = ["enero","febrero","marzo","abril","mayo","junio","julio",
          "agosto","septiembre","octubre","noviembre","diciembre"]
CAT_EMOJI = {"personal":"🌱","carrera profesional":"🚀","liderazgo":"🧭","desarrollo":"💻"}
# slug -> path, to rewrite internal cross-links
PATH_BY_SLUG = {slug: path for path, slug, _ in POSTS}

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")

def find_entry(doc):
    m = re.search(r'<div class="entry">', doc)
    start = m.end(); depth = 1
    for tok in re.finditer(r'<div\b|</div>', doc[start:]):
        if tok.group() == '</div>':
            depth -= 1
            if depth == 0:
                return doc[start:start + tok.start()]
        else:
            depth += 1
    return None

def meta(doc, name):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % re.escape(name), doc)
    return html.unescape(m.group(1)) if m else ""

def esc(s):
    return html.escape(s, quote=True)

def fmt_date(iso):
    y, m, d = int(iso[0:4]), int(iso[5:7]), int(iso[8:10])
    return f"{d} de {MONTHS[m-1]} de {y}", f"{iso[0:10]}"

def slugify_cat(c):
    return {"carrera profesional":"carrera","desarrollo":"desarrollo",
            "liderazgo":"liderazgo","personal":"personal"}[c]

# ── fetch + parse all posts ───────────────────────────────────────────
items = []
for path, slug, cat in POSTS:
    doc = fetch(f"{BASE}/{path}/")
    tm = re.search(r'<h3 class="article-title"><span>(.*?)</span></h3>', doc, re.S)
    title = html.unescape(tm.group(1).strip())
    dt = re.search(r'datetime="([^"]+)"', doc).group(1)
    rt = re.search(r'fa fa-clock-o">([^<]+)</span>', doc)
    read = rt.group(1).strip() if rt else ""
    desc = meta(doc, "description")
    body = find_entry(doc)
    items.append({"path": path, "slug": slug, "cat": cat, "title": title,
                  "dt": dt, "read": read, "desc": desc, "body": body})

# ── helpers to transform a post body ─────────────────────────────────
def transform_body(it):
    body = it["body"]
    # 1. drop the "read more" fold marker
    body = body.replace('<span id="more"></span>', '')
    # 2. download images, rewrite src to local filename
    post_dir = os.path.join(BLOG, it["slug"])
    os.makedirs(post_dir, exist_ok=True)
    for src in re.findall(r'<img[^>]+src="([^"]+)"', body):
        img_url = src if src.startswith("http") else BASE + src
        fname = os.path.basename(src.split("?")[0])
        data = fetch(img_url, binary=True)
        with open(os.path.join(post_dir, fname), "wb") as f:
            f.write(data)
        body = body.replace(f'src="{src}"', f'src="{fname}"')
        it["img"] = fname
    # add loading=lazy to imgs
    body = body.replace("<img ", '<img loading="lazy" ')
    # 3. rewrite internal cross-links to /blog/<slug>/
    def relink(m):
        target = m.group(1)
        mm = re.search(r'/(\d{4})/(\d{2})/([^/"]+)/?$', target)
        if mm and mm.group(3) in PATH_BY_SLUG:
            return f'href="/blog/{mm.group(3)}/"'
        return m.group(0)
    body = re.sub(r'href="(https?://javierdearcos\.com/\d{4}/\d{2}/[^"]+|/\d{4}/\d{2}/[^"]+)"', relink, body)
    return body.strip()

# ── per-post page template ───────────────────────────────────────────
def post_page(it, prev_it, next_it):
    long_date, iso_date = fmt_date(it["dt"])
    emoji = CAT_EMOJI[it["cat"]]
    og_img = f"{BASE}/blog/{it['slug']}/{it['img']}" if it.get("img") else ""
    pager = []
    if next_it:  # newer
        pager.append(f'<a class="pager-link pager-next" href="/blog/{next_it["slug"]}/">'
                     f'<span class="pager-dir">← Más reciente</span>'
                     f'<span class="pager-ttl">{esc(next_it["title"])}</span></a>')
    else:
        pager.append('<span></span>')
    if prev_it:  # older
        pager.append(f'<a class="pager-link pager-prev" href="/blog/{prev_it["slug"]}/">'
                     f'<span class="pager-dir">Más antiguo →</span>'
                     f'<span class="pager-ttl">{esc(prev_it["title"])}</span></a>')
    else:
        pager.append('<span></span>')
    return f'''<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(it["title"])} — Javier de Arcos</title>
  <meta name="description" content="{esc(it["desc"])}" />
  <meta name="author" content="Javier de Arcos" />
  <meta property="og:title" content="{esc(it["title"])}" />
  <meta property="og:description" content="{esc(it["desc"])}" />
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
    "headline": {json.dumps(it["title"], ensure_ascii=False)},
    "description": {json.dumps(it["desc"], ensure_ascii=False)},
    "datePublished": "{it["dt"]}",
    "author": {{ "@type": "Person", "name": "Javier de Arcos", "url": "{BASE}" }},
    "url": "{BASE}/blog/{it["slug"]}/"
  }}
  </script>
</head>
<body>
  <a href="#main" class="skip-link">Saltar al contenido</a>

  <nav class="nav" aria-label="Navegación principal">
    <a class="nav-logo" href="/">&gt;_ javierdearcos</a>
    <ul class="nav-links" id="navLinks" role="list">
      <li><a href="/">Inicio</a></li>
      <li><a href="/talks/">Charlas</a></li>
      <li><a href="/collabs/">Colaboraciones</a></li>
      <li><a href="/projects/">Proyectos</a></li>
      <li><a href="/blog/" aria-current="page">Blog</a></li>
      <li><a href="/contact/">Contacto</a></li>
    </ul>
    <div class="nav-controls">
      <button class="btn-icon" id="themeToggle" type="button" aria-label="Toggle theme">☀️</button>
      <button class="btn-icon nav-toggle" id="navToggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="navLinks">☰</button>
    </div>
  </nav>

  <main id="main">
    <div class="container">
      <article class="post">
        <header class="post-header">
          <a class="post-back" href="/blog/">← Todos los posts</a>
          <div class="post-meta">
            <span class="tag">{emoji} {esc(it["cat"])}</span>
            <time datetime="{iso_date}">{long_date}</time>
            <span class="post-read">· {esc(it["read"])} de lectura</span>
          </div>
          <h1 class="post-title-full">{esc(it["title"])}</h1>
        </header>
        <div class="post-body">
{it["html_body"]}
        </div>
      </article>

      <nav class="post-pager" aria-label="Más posts">
        {pager[0]}
        {pager[1]}
      </nav>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 Javier de Arcos · <a href="/">Inicio</a> · <a href="/blog/">Blog</a></p>
    </div>
  </footer>
</body>
</html>
'''

# ── blog index (listing) ─────────────────────────────────────────────
def index_page(items):
    rows = []
    for it in items:
        long_date, iso_date = fmt_date(it["dt"])
        emoji = CAT_EMOJI[it["cat"]]
        rows.append(f'''        <li class="post-entry" data-cat="{slugify_cat(it["cat"])}">
          <a class="post-entry-link" href="/blog/{it["slug"]}/">
            <div class="post-entry-meta">
              <span class="tag">{emoji} {esc(it["cat"])}</span>
              <time datetime="{iso_date}">{long_date}</time>
              <span class="post-read">· {esc(it["read"])}</span>
            </div>
            <h2 class="post-entry-title">{esc(it["title"])}</h2>
            <p class="post-entry-desc">{esc(it["desc"])}</p>
          </a>
        </li>''')
    rows_html = "\n".join(rows)
    cats = sorted({it["cat"] for it in items}, key=lambda c: list(CAT_EMOJI).index(c))
    filters = ['<button class="blog-filter is-active" data-filter="all" type="button">Todo</button>']
    for c in cats:
        filters.append(f'<button class="blog-filter" data-filter="{slugify_cat(c)}" type="button">{CAT_EMOJI[c]} {esc(c)}</button>')
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
  <a href="#main" class="skip-link">Saltar al contenido</a>

  <nav class="nav" aria-label="Navegación principal">
    <a class="nav-logo" href="/">&gt;_ javierdearcos</a>
    <ul class="nav-links" id="navLinks" role="list">
      <li><a href="/">Inicio</a></li>
      <li><a href="/talks/">Charlas</a></li>
      <li><a href="/collabs/">Colaboraciones</a></li>
      <li><a href="/projects/">Proyectos</a></li>
      <li><a href="/blog/" aria-current="page">Blog</a></li>
      <li><a href="/contact/">Contacto</a></li>
    </ul>
    <div class="nav-controls">
      <button class="btn-icon" id="themeToggle" type="button" aria-label="Toggle theme">☀️</button>
      <button class="btn-icon nav-toggle" id="navToggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="navLinks">☰</button>
    </div>
  </nav>

  <main id="main">
    <div class="container">
      <header class="blog-head">
        <p class="section-label">Escritos</p>
        <h1 class="blog-title">Blog</h1>
        <p class="blog-intro">Pienso escribiendo. Aquí comparto reflexiones sobre ingeniería, liderazgo, cultura de equipo y carrera profesional.</p>
      </header>

      <div class="blog-filters" role="group" aria-label="Filtrar por categoría">
        {filters_html}
      </div>

      <ul class="post-list" id="postList" role="list">
{rows_html}
      </ul>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 Javier de Arcos · <a href="/">Inicio</a> · <a href="/blog/">Blog</a></p>
    </div>
  </footer>
</body>
</html>
'''

# ── write everything ─────────────────────────────────────────────────
os.makedirs(BLOG, exist_ok=True)
# transform bodies first (downloads images, sets it["img"]) so page meta can use it
for it in items:
    it["html_body"] = transform_body(it)
for i, it in enumerate(items):
    newer = items[i-1] if i > 0 else None        # previous in list = newer
    older = items[i+1] if i < len(items)-1 else None
    pdir = os.path.join(BLOG, it["slug"])
    os.makedirs(pdir, exist_ok=True)
    page = post_page(it, prev_it=older, next_it=newer)
    with open(os.path.join(pdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)

with open(os.path.join(BLOG, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_page(items))

# emit featured-posts data (3 most recent) for the home page
featured = [{"slug": it["slug"], "title": it["title"], "cat": it["cat"],
             "desc": it["desc"], "emoji": CAT_EMOJI[it["cat"]],
             "year": it["dt"][:4]} for it in items[:3]]
json.dump(featured, open("/tmp/featured.json", "w"), ensure_ascii=False, indent=2)
print("Wrote", len(items), "post pages + index.")
print("Featured (home):", [f["slug"] for f in featured])
print("Images downloaded per post:", sum(1 for it in items if it.get("img")))

# ── redirect stubs for the old Hexo URLs (/YYYY/MM/slug/ → /blog/slug/) ──
# GitHub Pages has no server redirect rules, so each old path gets a static
# meta-refresh + canonical stub so existing links and SEO equity survive.
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
for path, slug, _ in POSTS:
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(STUB.format(base=BASE, slug=slug))
# custom apex domain + disable Jekyll so files serve as-is
with open(os.path.join(ROOT, "CNAME"), "w") as f:
    f.write("javierdearcos.com\n")
open(os.path.join(ROOT, ".nojekyll"), "w").close()
print("Wrote", len(POSTS), "redirect stubs + CNAME + .nojekyll")
