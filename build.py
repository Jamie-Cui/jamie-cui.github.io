#!/usr/bin/env python3
"""Build org-mode blog posts and assemble the site into _site/."""

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

SITE_DIR = Path("_site")
BLOG_DIR = Path("blogs")
PUBLISH_EL = Path("publish.el")

# Files and directories to copy to the output site
STATIC_FILES = ["index.html", "thumbnail.png", "LICENSE"]
STATIC_DIRS = ["imgs"]


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
    """Call Emacs batch to export a single org file to HTML."""
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


def inject_blog_list(index_path, posts):
    """Replace the blog-list marker region in index.html with a post list."""
    content = index_path.read_text(encoding="utf-8")

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

    blog_html = "\n".join(
        [
            "      <h2>Blogs</h2>",
            "",
            "      <ul>",
            "\n".join(items) if items else "        <li>No posts yet.</li>",
            "      </ul>",
        ]
    )

    new_content = re.sub(
        r"<!-- BLOG_LIST_START -->.*?<!-- BLOG_LIST_END -->",
        f"<!-- BLOG_LIST_START -->\n{blog_html}\n      <!-- BLOG_LIST_END -->",
        content,
        flags=re.DOTALL,
    )
    index_path.write_text(new_content, encoding="utf-8")


def main():
    print("Building site...")

    # Clean output directory
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()
    (SITE_DIR / "blogs").mkdir()

    # Copy static files and directories
    for name in STATIC_FILES:
        src = Path(name)
        if src.exists():
            shutil.copy2(src, SITE_DIR / name)
    for name in STATIC_DIRS:
        src = Path(name)
        if src.is_dir():
            shutil.copytree(src, SITE_DIR / name)

    # .nojekyll to prevent GitHub Pages Jekyll processing
    (SITE_DIR / ".nojekyll").touch()

    # Process org files
    posts = []
    if BLOG_DIR.is_dir():
        for org_file in sorted(BLOG_DIR.glob("*.org")):
            meta = parse_org_metadata(org_file)

            if meta.get("DRAFT", "").lower() in ("t", "true", "yes"):
                print(f"  skip draft: {org_file.name}")
                continue

            title = meta.get("TITLE", org_file.stem)
            date = meta.get("DATE", "")
            slug = meta.get("SLUG", make_slug(title, org_file.stem))

            output = SITE_DIR / "blogs" / f"{slug}.html"
            print(f"  export: {org_file.name} -> blogs/{slug}.html")

            if not export_org(org_file.resolve(), output.resolve()):
                sys.exit(1)

            posts.append({"title": title, "date": date, "slug": slug})

    # Sort by date, newest first
    posts.sort(key=lambda p: p["date"], reverse=True)

    # Inject blog list into index.html
    inject_blog_list(SITE_DIR / "index.html", posts)

    print(f"\nDone: {len(posts)} post(s) published to {SITE_DIR}/")


if __name__ == "__main__":
    main()
