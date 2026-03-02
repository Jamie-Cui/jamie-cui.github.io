# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal academic homepage for Jamie Cui, built with Jekyll. Fork of `jekyll-theme-minimal` (pages-themes/minimal). Hosted at https://jamie-cui.github.io/.

## Project Context

Primary languages in this workspace: Markdown, Python, Emacs Lisp. Documentation is often written in Chinese. LaTeX is used for academic papers.

## Workflow

Before making code edits or applying fixes, confirm the diagnosis and proposed approach with the user first. Do not jump straight to editing files.

## Commands

```bash
# Install dependencies
script/bootstrap

# Build site (outputs to _site/)
bundle exec jekyll build

# Local dev server
bundle exec jekyll serve

# Full CI pipeline (build, htmlproofer, rubocop, W3C validation, gem build)
script/cibuild
```

## Architecture

- `index.md` — Main homepage content (research interests, publications)
- `_config.yml` — Jekyll site config (title, theme, author)
- `_layouts/` — HTML templates (`default.html`, `post.html`)
- `_sass/` — SCSS stylesheets (theme styling, fonts, syntax highlighting)
- `assets/` — Static files (images, compiled CSS)
- `script/` — Build automation (`bootstrap`, `cibuild`, `release`)
- `jekyll-theme-minimal.gemspec` — Gem spec (also defines dev dependencies like html-proofer, rubocop, w3c_validators)

## Key Details

- Content is primarily in `index.md` using Markdown with Jekyll front matter
- The gemspec uses `git ls-files` to determine included files — new files must be tracked by git
- Rubocop config (`.rubocop.yml`) excludes `_site/` and disables line length checks
- CI validates HTML output with both htmlproofer (SRI checks enabled) and W3C validators

## Code Review

When asked to review or analyze a project, always operate on the full project/codebase unless explicitly told otherwise. Do not default to reviewing only the current diff or staged changes.

## Academic Writing

When writing academic/survey content (especially Related Work sections), provide precise positioning against the paper's specific contributions rather than generic summaries. Each cited work must be compared on concrete technical dimensions.
