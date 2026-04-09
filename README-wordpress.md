# Saneamientos — publicación WordPress (Markdown)

Mismo enfoque que LegalPin: login por cookies (navegador) y REST API para crear o actualizar posts desde Markdown. Útil si el sitio pasa por Cloudflare u otras capas donde un Application Password puro falla.

## Setup

```bash
cd saneamientos-wp
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env con WP_URL, WP_USER, WP_LOGIN_PASSWORD
```

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `WP_URL` | URL base del WordPress, sin barra final (ej. `https://www.tudominio.com`) |
| `WP_USER` | Usuario o email de WordPress |
| `WP_LOGIN_PASSWORD` | Contraseña de acceso a `wp-login.php` |

## Uso de `wp_publish.py`

```bash
# Borrador en español (por defecto)
python wp_publish.py article.md

# Publicar al momento
python wp_publish.py article.md --publish

# Idioma WPML
python wp_publish.py article.md --lang en

# Actualizar post existente
python wp_publish.py article.md --update 123
python wp_publish.py article.md --publish --update 123
```

## Frontmatter YAML

Ver `article-template.md`. Campos habituales: `title`, `slug`, `lang`, `categories`, `tags`, `excerpt`, `featured_image` (ruta relativa al `.md`).

**Nota:** Si el tema muestra el título del post como H1, no añadas otro `#` al inicio del cuerpo.

## WPML

Si está instalado el endpoint `wp-json/wpml/v1/set_language`, el script asigna el idioma tras crear o actualizar. Si no, asigna el idioma manualmente en el admin.

## Archivos

- `wp_publish.py` — publicador
- `article-template.md` — plantilla de artículo
- `saneamientos-urls.md` — catálogo de URLs para enlaces internos (rellenar cuando tengas el mapa del sitio)
