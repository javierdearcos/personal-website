# blog-src — fuente de contenido del blog (bilingüe)

Esta carpeta es la **fuente de verdad** del blog. Las páginas de `blog/<slug>/`
se generan a partir de aquí; **no edites las páginas generadas a mano**.

## Estructura por post

```
blog-src/<slug>/
  meta.json   metadatos (fecha, categoría, imagen, y título/desc/tiempo de lectura por idioma)
  es.html     cuerpo del artículo en español (fragmento HTML)
  en.html     cuerpo del artículo en inglés  (fragmento HTML; vacío = sin traducir)
```

### `meta.json`

```json
{
  "dt": "2025-10-10T00:00:00.000Z",
  "cat": "personal",                       // personal | carrera profesional | liderazgo | desarrollo
  "img": "portada.jpg",                    // opcional: nombre de la imagen og (vive en blog/<slug>/)
  "title": { "es": "...", "en": "..." },
  "desc":  { "es": "...", "en": "..." },
  "read":  { "es": "3 mins.", "en": "3 min" }
}
```

### `es.html` / `en.html`

Solo el **cuerpo** del post (sin `<html>`, `<head>` ni nav): párrafos `<p>`,
títulos `<h2>`, listas, `<figure><img src="archivo.jpg">`, etc. Las imágenes se
referencian por nombre y viven junto a la página generada en `blog/<slug>/`.

- Si `en.html` está **vacío**, la página muestra el cuerpo español con un aviso
  de "aún no traducido". Traduce el post escribiendo su HTML en `en.html`.
- Recuerda traducir también `title`, `desc` y `read` (campo `en`) en `meta.json`.

## Regenerar

```bash
python3 tools/build-blog.py     # regenera blog/<slug>/ y blog/index.html
```

El botón de idioma de la nav (ES/EN) alterna ambas versiones en el navegador y
recuerda la elección entre páginas. Los posts destacados de la home se editan
aparte en `data/posts.js` (campos `{ es, en }`).
