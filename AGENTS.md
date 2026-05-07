# Repository Guidelines

## Project Structure & Module Organization

This repository hosts a static personal academic site published to GitHub Pages. The root site is generated from Org mode sources: `src/index.org`, `src/research.org`, and posts in `src/blogs/*.org`. Shared styling lives in `site.css`, images in `imgs/`, and generated output in `_site/`. `build.py` exports Org fragments through `publish.el`, wraps them in the common HTML shell, builds the blog index, and copies static assets. Paper Feeds static assets live in `src/paper-feeds/`; its fetch/filter/summarize pipeline lives in `tools/paper-feeds/`. Follow `tools/paper-feeds/AGENTS.md` for that subproject.

## Build, Test, and Development Commands

- `python3 build.py` builds the deployable `_site/` directory. It requires Emacs with Org mode available.
- `python3 -m http.server 8080 -d _site` serves `_site/` at `http://127.0.0.1:8080/`.
- `pip install -r tools/paper-feeds/requirements.txt` installs Paper Feeds dependencies.
- `python tools/paper-feeds/scripts/main.py` refreshes Paper Feeds data; API keys may be required.

There is no root package manager or formal root test suite. Treat a successful `python3 build.py` run plus page inspection as primary validation.

## Coding Style & Naming Conventions

Keep root Python code compatible with Python 3 and use 4-space indentation. Prefer clear stdlib code over new dependencies. Org posts should include metadata such as `#+TITLE:`, `#+DATE:`, and optional `#+SLUG:`. Draft posts may use `#+DRAFT: t` and are skipped by the build. Blog URLs are `/blogs/{slug}.html`; use stable, lowercase ASCII slugs when setting them manually. Keep CSS minimal and consistent with the existing paper-like layout.

## Testing Guidelines

After changing Org sources, styles, or the build script, run `python3 build.py` and inspect relevant files under `_site/`. Check the homepage, research page, blog index, and any changed post. For Paper Feeds changes, validate generated data files and the static frontend as described in `tools/paper-feeds/AGENTS.md`.

## Commit & Pull Request Guidelines

Recent history uses short imperative messages, sometimes with Conventional Commit prefixes, for example `feat: add favicon.svg and link to all HTML pages`, `docs: Add link to BIBM 2024 paper`, and `Fix HTML injection in blog list: escape title and date values`. Keep commits focused and mention generated feed updates when applicable. Pull requests should summarize the user-visible change, list validation commands, link related issues, and include screenshots for visual changes.

## Security & Configuration Tips

Do not commit API keys, email credentials, or local environment files. GitHub Actions expects Paper Feeds secrets such as `MODELSCOPE_API_KEY`, `DASHSCOPE_API_KEY`, `EMAIL_USERNAME`, `EMAIL_PASSWORD`, and `EMAIL_TO`.
