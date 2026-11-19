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
PAPER_PDF = ROOT / "output/pdf/sixfold-draft.pdf"
VISUALS = json.loads((ROOT / "verification/visuals-edition-01.json").read_text(encoding="utf-8"))
GALLERY = ROOT / VISUALS["library"]
PAGES = [
    ("definition", "Definition"),
    ("results", "Results & evidence"),
    ("related", "Published relatives"),
    ("reproduce", "Reproduce"),
    ("media", "Images & films"),
    ("paper", "Paper draft"),
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
        elif path == PAPER_PDF:
            destination = "paper/sixfold-draft.pdf"
        elif path.is_relative_to(ROOT / "site/assets"):
            destination = "assets/" + path.relative_to(ROOT / "site/assets").as_posix()
        elif path.is_relative_to(GALLERY):
            destination = "gallery/" + path.relative_to(GALLERY).as_posix()
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
    youtube_id = media.get("youtube_id", "")
    if video_url and youtube_id:
        raise ValueError("Choose either video_url or youtube_id.")
    poster_url = html.escape(media.get("poster", "assets/sixfold.png"), quote=True)
    title = html.escape(media["title"], quote=True)
    poster = f'<img src="{poster_url}" alt="{title}" width="1280" height="720">'
    if video_url:
        parsed = urlsplit(video_url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("video_url must be a public HTTPS URL.")
        return (f'<video controls playsinline preload="none" aria-label="{title}, a silent Sixfold film" poster="{poster_url}" width="1280" height="720">'
                f'<source src="{html.escape(video_url, quote=True)}" type="video/mp4">'
                'Your browser does not support this video.</video>')
    if youtube_id:
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", youtube_id):
            raise ValueError("youtube_id must be an 11-character video ID.")
        return poster + f'<button class="play-film" data-youtube-id="{youtube_id}">Play film</button>'
    return poster


def build_gallery():
    target = OUTPUT / "gallery"
    shutil.copytree(GALLERY, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.mp4", "*.partial"))
    page = (GALLERY / "index.html").read_text(encoding="utf-8")
    page = page.replace("Sixfold — Select your favourites", "Sixfold — Films & gallery")
    page = page.replace('<div class="eyebrow">', '<p><a href="../index.html">← Sixfold home</a> · <a href="#films">Watch the films</a> · <a href="' + VISUALS['release_url'] + '">Download this edition</a></p><div class="eyebrow">', 1)
    page = page.replace('Mark favourites, then download your selection or send the image numbers.', 'Mark favourites and save a list of your selections. Images and films are available to reuse with credit to okwhynot-wtf under CC BY 4.0.')
    page = page.replace('<h2>Motion studies</h2>', '<h2 id="films">Motion studies</h2>')
    for film in VISUALS['films']:
        local_path = Path(film['path']).relative_to(Path(VISUALS['library'])).as_posix()
        if page.count('src="' + local_path + '"') != 1:
            raise ValueError(f"Expected one video reference for {local_path}")
        page = page.replace('src="' + local_path + '"', 'src="' + html.escape(film['url'], quote=True) + '"')
    page = page.replace('<video controls ', '<video controls playsinline ')
    page = page.replace('<footer>', '<footer><p>By <a href="https://github.com/okwhynot-wtf">okwhynot-wtf</a>, with GPT assistance. <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> · <a href="../media.html">Rendering and credits</a></p>')
    (target / 'index.html').write_text(page, encoding='utf-8')


def main():
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "paper").mkdir(exist_ok=True)
    shutil.copy2(PAPER_PDF, OUTPUT / "paper/sixfold-draft.pdf")
    shutil.copytree(ROOT / "site/assets", OUTPUT / "assets", dirs_exist_ok=True)
    build_gallery()
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    media = json.loads((ROOT / "site/media.json").read_text(encoding="utf-8"))
    home = (ROOT / "site/templates/home.html").read_text(encoding="utf-8")
    for key in ("hero", "loops"):
        home = home.replace("{{" + key + "_film}}", film_markup(media[key]))
        home = home.replace("{{" + key + "_caption}}", html.escape(media[key]["caption"]))
    studies = "".join(
        '<figure><div class="film-frame">' + film_markup(film) + '</div>'
        '<figcaption><h3>' + html.escape(film["title"]) + '</h3><p>'
        + html.escape(film["caption"]) + '</p></figcaption></figure>'
        for film in media["studies"]
    )
    home = home.replace("{{studies}}", studies)
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
    print(f"Built homepage, gallery and {len(PAGES)} research pages in {OUTPUT}.")
    print("All documentation source links resolve.")


if __name__ == "__main__":
    main()
