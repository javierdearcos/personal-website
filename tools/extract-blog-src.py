#!/usr/bin/env python3
"""One-time bootstrap: extract the current (Spanish) blog pages under blog/<slug>/
into editable per-language sources under blog-src/<slug>/.

For each post it writes:
  blog-src/<slug>/meta.json   metadata, with title/desc/read split per language
  blog-src/<slug>/es.html     the Spanish body fragment (extracted as-is)
  blog-src/<slug>/en.html     EMPTY placeholder — write the English translation here

After running this once, blog-src/ becomes the source of truth and pages are
(re)generated with tools/build-blog.py. This script is not meant to be re-run;
it only reconstructs sources from already-generated pages.
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
SRC = os.path.join(ROOT, "blog-src")

# emoji prefix on the category tag -> canonical category name
EMOJI_CAT = {"🌱": "personal", "🚀": "carrera profesional",
             "🧭": "liderazgo", "💻": "desarrollo"}


def grab(pattern, doc, flags=0, default=""):
    m = re.search(pattern, doc, flags)
    return m.group(1) if m else default


def extract(slug):
    path = os.path.join(BLOG, slug, "index.html")
    with open(path, encoding="utf-8") as f:
        doc = f.read()

    title = html.unescape(grab(r'<h1 class="post-title-full">(.*?)</h1>', doc, re.S).strip())
    desc = html.unescape(grab(r'<meta name="description" content="([^"]*)"', doc))
    dt = grab(r'<meta property="article:published_time" content="([^"]+)"', doc)
    tag = grab(r'<span class="tag">(.*?)</span>', doc, re.S).strip()
    emoji = tag.split(" ", 1)[0]
    cat = EMOJI_CAT.get(emoji, "personal")
    read = grab(r'<span class="post-read">·\s*(.*?)\s*de lectura</span>', doc, re.S).strip()
    img = grab(r'<meta property="og:image" content="[^"]*/([^"/]+)"', doc)

    body = grab(r'<div class="post-body">\s*(.*?)\s*</div>\s*</article>', doc, re.S).strip()

    meta = {
        "dt": dt,
        "cat": cat,
        # title / desc / read are split per language; EN starts as a copy of ES
        # so the build works immediately. Edit the "en" values when you translate.
        "title": {"es": title, "en": title},
        "desc": {"es": desc, "en": desc},
        "read": {"es": read, "en": read},
    }
    if img:
        meta["img"] = img

    out = os.path.join(SRC, slug)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(out, "es.html"), "w", encoding="utf-8") as f:
        f.write(body + "\n")
    en_path = os.path.join(out, "en.html")
    if not os.path.exists(en_path):
        with open(en_path, "w", encoding="utf-8") as f:
            f.write("")  # empty -> build falls back to ES with an "untranslated" notice
    return slug


slugs = [d for d in os.listdir(BLOG)
         if os.path.isfile(os.path.join(BLOG, d, "index.html")) and d != "index.html"]
for slug in sorted(slugs):
    extract(slug)
    print("extracted", slug)
print(f"\nWrote {len(slugs)} sources to blog-src/. Edit each en.html to translate.")
