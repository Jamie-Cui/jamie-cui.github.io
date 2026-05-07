#!/usr/bin/env python3
"""Build org-mode pages and blog posts into _site/."""

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SITE_DIR = Path("_site")
SRC_DIR = Path("src")
BLOG_DIR = SRC_DIR / "blogs"
PAPER_FEEDS_DIR = SRC_DIR / "paper-feeds"
PUBLISH_EL = Path("publish.el")

# Files and directories to copy to the output site
STATIC_FILES = ["site.css", "favicon.svg", "LICENSE"]
STATIC_DIRS = ["imgs"]

NAV_ITEMS = [
    ("/", "Home"),
    ("/research/", "Research"),
    ("/blogs/", "Blogs"),
    ("/paper-feeds/", "Paper Feeds"),
]

PAGES = [
    {
        "source": SRC_DIR / "index.org",
        "output": SITE_DIR / "index.html",
        "title": "Jamie Cui",
        "subtitle": "",
        "profile": True,
    },
    {
        "source": SRC_DIR / "research.org",
        "output": SITE_DIR / "research" / "index.html",
        "title": "Research - Jamie Cui",
        "subtitle": "Research",
        "profile": False,
    },
]


def parse_org_metadata(filepath):
    """Extract #+KEY: VALUE pairs from the org file header."""
    metadata = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"#\+(\w+):\s*(.*)", line)
            if m:
                metadata[m.group(1).upper()] = m.group(2).strip()
            elif not line.startswith("#") and line.strip():
                break  # stop at first non-comment, non-blank line
    return metadata


def make_slug(title, filename_stem):
    """Generate a URL-safe slug from a title, falling back to filename stem."""
    # Keep only ASCII alphanumeric chars; replace everything else with hyphens
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()
    slug = re.sub(r"-+", "-", slug)
    if len(slug) < 3:
        slug = filename_stem
    return slug


def export_org(org_path, output_path):
    """Call Emacs batch to export a single org file to an HTML fragment."""
    el = str(PUBLISH_EL.resolve())
    org_s = str(org_path).replace("\\", "\\\\").replace('"', '\\"')
    out_s = str(output_path).replace("\\", "\\\\").replace('"', '\\"')

    cmd = [
        "emacs",
        "--batch",
        "--no-init-file",
        "--load",
        el,
        "--eval",
        f'(blog-export-file "{org_s}" "{out_s}")',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR exporting {org_path.name}:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False
    return True


def export_org_fragment(org_path, fragment_dir):
    """Export ORG_PATH to a temporary HTML fragment and return its contents."""
    rel = org_path.relative_to(SRC_DIR)
    fragment_path = fragment_dir / rel.with_suffix(".html")
    fragment_path.parent.mkdir(parents=True, exist_ok=True)

    if not export_org(org_path.resolve(), fragment_path.resolve()):
        sys.exit(1)

    return strip_volatile_org_ids(fragment_path.read_text(encoding="utf-8").strip())


def strip_volatile_org_ids(content):
    """Remove org-html's generated headline IDs from body fragments."""
    content = re.sub(r' id="outline-container-org[0-9a-f]+"', "", content)
    content = re.sub(r' id="text-org[0-9a-f]+"', "", content)
    return re.sub(r' id="org[0-9a-f]+"', "", content)


def render_nav():
    """Render the shared section navigation."""
    links = [
        f'      <a class="tag" href="{href}">{html.escape(label)}</a>'
        for href, label in NAV_ITEMS
    ]
    return '\n    <nav class="tags" aria-label="Sections">\n' + "\n".join(links) + "\n    </nav>"


def render_header(subtitle="", profile=False):
    """Render the shared page header."""
    if profile:
        return """    <header class="profile-header">
      <img src="/imgs/avatar.jpg" alt="Jamie Cui" class="avatar">
      <div>
        <h1><a href="/">Jamie Cui</a></h1>
        <p class="subtitle">jamie [dot] cui [at] outlook [dot] com</p>
        <p><a href="https://github.com/Jamie-Cui">GitHub</a></p>
      </div>
    </header>"""

    subtitle_html = (
        f'\n      <p class="subtitle">{html.escape(subtitle)}</p>' if subtitle else ""
    )
    return f"""    <header>
      <h1><a href="/">Jamie Cui</a></h1>{subtitle_html}
    </header>"""


def render_page(page_title, body_html, subtitle="", profile=False):
    """Wrap body HTML in the site's shared document shell."""
    return f"""<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(page_title)}</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="stylesheet" href="/site.css">
  </head>
  <body>
{render_header(subtitle, profile)}

{render_nav()}

    <main>
{indent_html(body_html, 6)}
    </main>

    <footer>
      <p>It is possible to build a cabin with no foundations, but not a lasting building.</p>
    </footer>
  </body>
</html>
"""


def indent_html(content, spaces):
    """Indent a block of generated HTML for readable output."""
    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in content.splitlines()) + "\n"


def write_page(path, content):
    """Write a complete HTML page."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_blog_index(posts):
    """Render the blog index page contents."""

    items = []
    for p in posts:
        title_escaped = html.escape(p["title"])
        date_span = (
            f' <span style="color:#555">({html.escape(p["date"])})</span>'
            if p["date"]
            else ""
        )
        items.append(
            f'        <li><a href="/blogs/{p["slug"]}.html">{title_escaped}</a>{date_span}</li>'
        )

    return "\n".join(
        [
            "<h2>Blogs</h2>",
            "",
            "<ul>",
            "\n".join(items) if items else "        <li>No posts yet.</li>",
            "</ul>",
        ]
    )


def render_post(title, date, author, body_html):
    """Render a blog post body."""
    meta = []
    if date:
        meta.append(f'<p class="date">{html.escape(date)}</p>')
    if author:
        meta.append(f'<p class="author">{html.escape(author)}</p>')

    return "\n".join(
        [
            "<article>",
            f"  <h1>{html.escape(title)}</h1>",
            *[f"  {line}" for line in meta],
            indent_html(body_html, 2).rstrip(),
            "</article>",
        ]
    )


def copy_paper_feeds():
    """Copy the Paper Feeds frontend into the output site."""
    dest_dir = SITE_DIR / "paper-feeds"
    if not PAPER_FEEDS_DIR.is_dir():
        return

    shutil.copytree(PAPER_FEEDS_DIR, dest_dir)


def main():
    print("Building site...")

    # Clean output directory
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    # Copy static files and directories
    for name in STATIC_FILES:
        src = Path(name)
        if src.exists():
            shutil.copy2(src, SITE_DIR / name)
    for name in STATIC_DIRS:
        src = Path(name)
        if src.is_dir():
            shutil.copytree(src, SITE_DIR / name)
    copy_paper_feeds()

    # .nojekyll to prevent GitHub Pages Jekyll processing
    (SITE_DIR / ".nojekyll").touch()

    with tempfile.TemporaryDirectory() as tmp:
        fragment_dir = Path(tmp)

        # Export regular pages from src/*.org
        for page in PAGES:
            source = page["source"]
            if not source.exists():
                print(f"  missing page source: {source}", file=sys.stderr)
                sys.exit(1)

            print(f"  export: {source} -> {page['output'].relative_to(SITE_DIR)}")
            body = export_org_fragment(source, fragment_dir)
            write_page(
                page["output"],
                render_page(
                    page["title"],
                    body,
                    subtitle=page["subtitle"],
                    profile=page["profile"],
                ),
            )

        # Process blog org files
        posts = []
        if BLOG_DIR.is_dir():
            for org_file in sorted(BLOG_DIR.glob("*.org")):
                meta = parse_org_metadata(org_file)

                if meta.get("DRAFT", "").lower() in ("t", "true", "yes"):
                    print(f"  skip draft: {org_file.name}")
                    continue

                title = meta.get("TITLE", org_file.stem)
                date = meta.get("DATE", "")
                author = meta.get("AUTHOR", "")
                slug = meta.get("SLUG", make_slug(title, org_file.stem))

                output = SITE_DIR / "blogs" / f"{slug}.html"
                print(f"  export: {org_file} -> blogs/{slug}.html")

                body = export_org_fragment(org_file, fragment_dir)
                post_html = render_post(title, date, author, body)
                write_page(
                    output,
                    render_page(
                        f"{title} - Jamie Cui",
                        post_html,
                        subtitle="Blog",
                        profile=False,
                    ),
                )

                posts.append({"title": title, "date": date, "slug": slug})

    # Sort by date, newest first
    posts.sort(key=lambda p: p["date"], reverse=True)

    write_page(
        SITE_DIR / "blogs" / "index.html",
        render_page("Blogs - Jamie Cui", render_blog_index(posts), subtitle="Blogs"),
    )

    print(f"\nDone: {len(posts)} post(s) published to {SITE_DIR}/")


if __name__ == "__main__":
    main()
