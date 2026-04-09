#!/usr/bin/env python3
"""
wp_publish.py — WordPress Publisher for Saneamientos (cookie-based auth)
Bypasses Cloudflare by logging in like a real browser.

Usage:
  python wp_publish.py article.md                        # create as draft (ES)
  python wp_publish.py article.md --publish               # publish immediately
  python wp_publish.py article.md --lang en               # create in English
  python wp_publish.py article.md --update 123            # update existing post
  python wp_publish.py article.md --publish --update 123  # update and publish

YAML frontmatter fields:
  title, slug, excerpt, categories, tags, featured_image, lang (es|en|fr)
"""

import os
import sys
import re
import argparse
import mimetypes
from pathlib import Path

import requests
import markdown
import yaml
from dotenv import load_dotenv

load_dotenv()

WP_URL        = os.getenv("WP_URL", "").rstrip("/")
WP_USER       = os.getenv("WP_USER", "")
WP_LOGIN_PASS = os.getenv("WP_LOGIN_PASSWORD", "")

if not all([WP_URL, WP_USER, WP_LOGIN_PASS]):
    print("❌  Missing credentials. Make sure .env has WP_URL, WP_USER, WP_LOGIN_PASSWORD.")
    sys.exit(1)

API = f"{WP_URL}/wp-json/wp/v2"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept":          "application/json, text/html, */*",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8,fr;q=0.7",
    "Referer":         f"{WP_URL}/wp-admin/",
}


def make_session() -> requests.Session:
    """Log in to WordPress like a browser, return authenticated session."""
    session = requests.Session()
    session.headers.update(HEADERS)

    print("🔐  Logging in to WordPress...")

    domain = WP_URL.split("//")[-1].split("/")[0]
    session.cookies.set("wordpress_test_cookie", "WP Cookie check", domain=domain)

    login_data = {
        "log":         WP_USER,
        "pwd":         WP_LOGIN_PASS,
        "wp-submit":   "Log In",
        "redirect_to": f"{WP_URL}/wp-admin/",
        "testcookie":  "1",
    }

    r = session.post(f"{WP_URL}/wp-login.php", data=login_data, allow_redirects=True)

    if "wp-admin" not in r.url and "dashboard" not in r.text.lower():
        print(f"❌  Login failed — check WP_USER and WP_LOGIN_PASSWORD in .env")
        print(f"    Status: {r.status_code} | Landed at: {r.url}")
        sys.exit(1)

    print("✅  Logged in")

    nonce = ""
    nonce_r = session.get(f"{WP_URL}/wp-admin/admin-ajax.php", params={"action": "rest-nonce"})
    if nonce_r.ok and re.match(r"^[a-f0-9]+$", nonce_r.text.strip()):
        nonce = nonce_r.text.strip()
    else:
        page_r = session.get(f"{WP_URL}/wp-admin/post-new.php")
        for pattern in [r'"nonce":"([a-f0-9]+)"', r'wpApiSettings[^}]*"nonce"\s*:\s*"([a-f0-9]+)"']:
            m = re.search(pattern, page_r.text)
            if m:
                nonce = m.group(1)
                break

    if nonce:
        print(f"🔑  Nonce obtained")
        session.headers["X-WP-Nonce"] = nonce
    else:
        print("⚠️  Could not get nonce — some API calls may fail")

    return session


def parse_md(filepath: Path) -> tuple[dict, str]:
    """Split YAML frontmatter and Markdown body."""
    text = filepath.read_text(encoding="utf-8")
    m = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL).match(text)
    if m:
        return yaml.safe_load(m.group(1)) or {}, text[m.end():]
    return {}, text


def md_to_html(body: str) -> str:
    return markdown.markdown(body, extensions=["extra", "codehilite", "toc", "nl2br"])


def get_or_create_terms(session: requests.Session, names: list[str], taxonomy: str) -> list[int]:
    endpoint = f"{API}/{'categories' if taxonomy == 'category' else 'tags'}"
    ids = []
    for name in [n.strip() for n in names]:
        r = session.get(endpoint, params={"search": name})
        results = r.json() if r.ok else []
        existing = next((t for t in results if t["name"].lower() == name.lower()), None)
        if existing:
            ids.append(existing["id"])
        else:
            r = session.post(endpoint, json={"name": name})
            if r.ok:
                ids.append(r.json()["id"])
                print(f"  ✚ Created {taxonomy}: {name}")
            else:
                print(f"  ⚠ Could not create {taxonomy} '{name}'")
    return ids


def upload_image(session: requests.Session, image_path: Path) -> int | None:
    if not image_path.exists():
        print(f"  ⚠ Image not found: {image_path}")
        return None
    mime = mimetypes.guess_type(str(image_path))[0] or "image/jpeg"
    r = session.post(
        f"{API}/media",
        headers={"Content-Disposition": f'attachment; filename="{image_path.name}"', "Content-Type": mime},
        data=image_path.read_bytes(),
    )
    if r.ok:
        mid = r.json()["id"]
        print(f"  🖼  Uploaded: {image_path.name} (ID {mid})")
        return mid
    print(f"  ⚠ Image upload failed: {r.status_code}")
    return None


def set_wpml_language(session: requests.Session, post_id: int, lang: str):
    r = session.post(f"{WP_URL}/wp-json/wpml/v1/set_language", json={"post_id": post_id, "language": lang})
    if r.ok:
        print(f"  🌐  WPML language: {lang.upper()}")
    else:
        print(f"  ⚠  Set language manually in WP Admin (lang={lang})")


def build_payload(session: requests.Session, meta: dict, html: str, publish: bool, md_file: Path, lang: str) -> dict:
    effective_lang = meta.get("lang", lang)
    payload: dict = {
        "title":   meta.get("title", md_file.stem.replace("-", " ").title()),
        "content": html,
        "status":  "publish" if publish else "draft",
        "lang":    effective_lang,
    }
    if "slug"    in meta: payload["slug"]    = meta["slug"]
    if "excerpt" in meta: payload["excerpt"] = meta["excerpt"]

    if "categories" in meta:
        cats = meta["categories"]
        payload["categories"] = get_or_create_terms(session, [cats] if isinstance(cats, str) else cats, "category")

    if "tags" in meta:
        tags = meta["tags"]
        payload["tags"] = get_or_create_terms(session, [tags] if isinstance(tags, str) else tags, "post_tag")

    if meta.get("featured_image"):
        img_val  = str(meta["featured_image"]).strip()
        img_path = Path(img_val) if Path(img_val).exists() else md_file.parent / img_val
        if img_path.exists():
            mid = upload_image(session, img_path)
            if mid: payload["featured_media"] = mid
        elif img_val.startswith("http"):
            print("  ℹ  featured_image is a URL — skipping upload")

    return payload


def main():
    parser = argparse.ArgumentParser(description="Publish Markdown to WordPress")
    parser.add_argument("file")
    parser.add_argument("--publish", action="store_true", help="Publish immediately (default: draft)")
    parser.add_argument("--update",  type=int, metavar="POST_ID", help="Update existing post by ID")
    parser.add_argument("--lang",    default="es", choices=["es", "en", "fr"], help="WPML language (default: es)")
    args = parser.parse_args()

    md_file = Path(args.file)
    if not md_file.exists():
        print(f"❌  File not found: {md_file}")
        sys.exit(1)

    session        = make_session()
    meta, body     = parse_md(md_file)
    html           = md_to_html(body)
    payload        = build_payload(session, meta, html, args.publish, md_file, args.lang)
    effective_lang = meta.get("lang", args.lang)
    status_label   = "publish" if args.publish else "draft"

    print(f"\n📄  {md_file.name} → [{status_label}] [{effective_lang.upper()}]")

    if args.update:
        r = session.post(f"{API}/posts/{args.update}", json=payload)
        if r.ok:
            print(f"✅  Updated post #{args.update}")
            print(f"    🔗 {r.json().get('link', '')}")
            set_wpml_language(session, args.update, effective_lang)
        else:
            print(f"❌  Update failed: {r.status_code}\n{r.text}")
            sys.exit(1)
    else:
        r = session.post(f"{API}/posts", json=payload)
        if r.ok:
            post    = r.json()
            post_id = post["id"]
            print(f"✅  Created post #{post_id}")
            print(f"    🔗 {post.get('link', '')}")
            set_wpml_language(session, post_id, effective_lang)
            print(f"\n    💡 To update: python wp_publish.py {md_file} --update {post_id}")
        else:
            print(f"❌  Create failed: {r.status_code}\n{r.text}")
            sys.exit(1)


if __name__ == "__main__":
    main()
