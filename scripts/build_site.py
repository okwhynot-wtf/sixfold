"""Build GitHub Pages from the canonical Markdown documentation."""

import html
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote, unquote, urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"
REPOSITORY = "https://github.com/okwhynot-wtf/sixfold/blob/main/"
PAGES = [
    ("definition", "Definition"),
    ("results", "Results & evidence"),
    ("related", "Published relatives"),
    ("reproduce", "Reproduce"),
    ("media", "Images & films"),
    ("paper", "Paper source map"),
    ("provenance", "Credits & AI"),
    ("release", "Release & DOI"),
]


def rewrite_links(content, source):
    def replace(match):
        attribute, value = match.groups()
        url = urlsplit(html.unescape(value))
        if url.scheme or url.netloc or not url.path:
            return match.group(0)
        path = (source.parent / unquote(url.path)).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f"Broken source link in {source.name}: {value}")
        if path.parent == ROOT / "docs":
            destination = path.stem + ".html"
        elif path.is_relative_to(ROOT / "site/assets"):
            destination = "assets/" + path.relative_to(ROOT / "site/assets").as_posix()
        else:
            destination = REPOSITORY + quote(path.relative_to(ROOT).as_posix())
        if url.fragment:
            destination += "#" + url.fragment
        return f'{attribute}="{html.escape(destination, quote=True)}"'
    return re.sub(r'(href|src)="([^"]+)"', replace, content)


def render_page(title, description, content, document=False):
    template = (ROOT / "site/templates/layout.html").read_text(encoding="utf-8")
    math = ""
    if document:
        math = ('<script src="assets/math.js"></script>'
                '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>')
    values = {
        "title": html.escape(title),
        "description": html.escape(description, quote=True),
        "body_class": "document" if document else "home",
        "content": content,
        "math": math,
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def film_markup(media):
    video_url = media["video_url"]
    youtube_id = media["youtube_id"]
    if video_url and youtube_id:
        raise ValueError("Choose either video_url or youtube_id.")
    poster = '<img src="assets/sixfold.png" alt="Six interlocking lobes of the reference fractal in copper and teal" width="1280" height="720" fetchpriority="high">'
    if video_url:
        parsed = urlsplit(video_url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("video_url must be a public HTTPS URL.")
        return ('<video controls playsinline preload="none" poster="assets/sixfold.png">'
                f'<source src="{html.escape(video_url, quote=True)}" type="video/mp4">'
                'Your browser does not support this video.</video>')
    if youtube_id:
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", youtube_id):
            raise ValueError("youtube_id must be an 11-character video ID.")
        return poster + f'<button class="play-film" data-youtube-id="{youtube_id}">Play film</button>'
    return poster


def main():
    OUTPUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "site/assets", OUTPUT / "assets", dirs_exist_ok=True)
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    media = json.loads((ROOT / "site/media.json").read_text(encoding="utf-8"))
    home = (ROOT / "site/templates/home.html").read_text(encoding="utf-8")
    home = home.replace("{{film}}", film_markup(media))
    home = home.replace("{{caption}}", html.escape(media["caption"]))
    (OUTPUT / "index.html").write_text(render_page(
        "Sixfold — a family of self-similar spatial fractals",
        "Explore a six-copy spatial fractal through its exact definition, reproducible research and copper-and-teal visualisations.",
        home), encoding="utf-8")
    for slug, label in PAGES:
        source = ROOT / "docs" / f"{slug}.md"
        content = markdown.markdown(
            source.read_text(encoding="utf-8"),
            extensions=["tables", "fenced_code", "toc", "pymdownx.arithmatex", "pymdownx.tasklist"],
            extension_configs={"pymdownx.arithmatex": {"generic": True}},
        )
        content = rewrite_links(content, source)
        navigation = "".join(
            f'<a href="{name}.html"'
            + (' aria-current="page"' if name == slug else '')
            + f'>{html.escape(text)}</a>'
            for name, text in PAGES
        )
        source_url = REPOSITORY + f"docs/{slug}.md"
        body = (f'<main id="main" class="document-shell wrap">'
                f'<aside class="sidebar"><nav aria-label="Research pages">{navigation}</nav></aside>'
                f'<article class="article"><div class="source-link">'
                f'<a href="{source_url}">Read or suggest a correction on GitHub ↗</a></div>'
                f'{content}</article></main>')
        (OUTPUT / f"{slug}.html").write_text(render_page(
            f"{label} — Sixfold", f"Sixfold research documentation. {label}.",
            body, document=True), encoding="utf-8")
    print(f"Built homepage and {len(PAGES)} research pages in {OUTPUT}.")
    print("All documentation source links resolve.")


if __name__ == "__main__":
    main()
