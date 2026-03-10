# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal academic homepage for Jamie Cui (PhD candidate at ECNU) with org-mode blog support. Hosted at https://jamie-cui.github.io/ via GitHub Pages (deployed by GitHub Actions).

## Project Context

Primary languages in this workspace: Markdown, Python, Emacs Lisp. Documentation is often written in Chinese. LaTeX is used for academic papers.

## Workflow

Before making code edits or applying fixes, confirm the diagnosis and proposed approach with the user first. Do not jump straight to editing files.

## Commands

```bash
# Build site (requires Emacs): exports org posts, injects blog list, outputs to _site/
python3 build.py

# Local preview (after build)
python3 -m http.server 8080 -d _site
```

## Architecture

- `index.html` — Homepage with inline CSS. Blog list is auto-injected between `<!-- BLOG_LIST_START -->` and `<!-- BLOG_LIST_END -->` markers by `build.py`
- `blogs/*.org` — Blog posts in org-mode format. Metadata via `#+TITLE`, `#+DATE`, `#+AUTHOR`, `#+DRAFT`, `#+SLUG`
- `build.py` — Build script: scans org files, skips drafts (`#+DRAFT: t`), calls Emacs batch to export HTML, generates blog list, copies everything to `_site/`
- `publish.el` — Emacs Lisp config for org-html export: inline CSS matching the paper style, nav header, footer, date/author display
- `.github/workflows/deploy.yml` — CI: installs emacs-nox, runs `build.py`, deploys `_site/` to GitHub Pages

## Key Details

- The site uses a minimal "paper" aesthetic: Georgia/serif font, 800px max-width, black text on white
- Blog post URLs: `/blogs/{slug}.html` where slug is auto-generated from title (ASCII chars only) or set explicitly via `#+SLUG:`
- Posts with `#+DRAFT: t` are skipped entirely (no HTML generated, no listing)
- CSS is inline in both `index.html` and each exported blog post (defined in `publish.el` `blog-css` variable) — keep them in sync
- `_site/` is gitignored; it's built fresh by CI on each push to master

## Code Review

When asked to review or analyze a project, always operate on the full project/codebase unless explicitly told otherwise. Do not default to reviewing only the current diff or staged changes.

## Academic Writing

When writing academic/survey content (especially Related Work sections), provide precise positioning against the paper's specific contributions rather than generic summaries. Each cited work must be compared on concrete technical dimensions.
