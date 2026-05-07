# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Paper Feeds** is a keyword-based research paper aggregator that fetches papers from arXiv and IACR ePrint, filters by configurable keywords, generates bilingual (Chinese/English) AI summaries via Alibaba's DashScope API (Qwen), and displays results on a static GitHub Pages site. Runs daily via GitHub Actions.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the paper fetcher (requires API key)
export DASHSCOPE_API_KEY="your-key"   # or MODELSCOPE_API_KEY
python scripts/main.py

# View results locally: open index.html in a browser
# Data outputs: data/papers.json, data/failed.json
```

There are no tests, linting, or build steps. The GitHub Actions workflow runs on Python 3.11.

## Architecture

### Pipeline (scripts/main.py)

The pipeline runs sequentially: **Fetch → Filter → Summarize → Merge → Save → RSS**.

1. **Fetch** — `scripts/fetchers/arxiv.py` (arXiv API, XML parsing) and `scripts/fetchers/iacr.py` (RSS via feedparser). Both respect per-source rate limit delays configured in `config.toml`.

2. **Filter** — `scripts/filter.py` uses `keywords.txt` with OR logic between lines and AND logic within a line. Uses `\b` word-boundary regex, case-insensitive, matching against title + abstract. Filtering can be independently enabled/disabled per source via `apply_to_arxiv` and `apply_to_iacr` in `config.toml`.

3. **Summarize** — `scripts/summarizer.py` (`ModelScopeSummarizer`) makes one DashScope API call per paper producing both Chinese and English summaries. The bilingual prompt is hard-coded in `_create_bilingual_prompt()` (not from `config.toml`). Output is parsed by `_parse_bilingual_summary()` using `[中文摘要]` and `[English Summary]` section markers with regex. Do NOT change these markers without updating the parser. Failed papers retry with exponential backoff (configurable retries/delay) and fall back to abstract text.

4. **Merge & Save** — Deduplicates by paper ID, removes papers older than `days_back` (configured in `config.toml`, currently 30 days), sorts by date descending. Previously failed summaries are retried each run.

5. **RSS** — `scripts/rss.py` generates `feed.xml` (RSS 2.0) in the project root after saving. Uses English summary as item description, falls back to abstract. Limited to `max_items` (default 50) most recent papers. Requires `site_url` in `config.toml` for absolute feed links. Uses only stdlib (`xml.etree.ElementTree`).

### Frontend (index.html, app.js, styles.css, config.js)

Static site served from repo root via GitHub Pages (master branch, `/` directory). Client-side search/filter/sort with pagination. Key features:
- Pagination: configurable via `papers_per_page` in `config.toml` (default 10), generated to `config.js` by `scripts/generate_config.py`
- Bilingual summary toggle (中/EN buttons) per card via `toggleLanguage(index, lang)` in `app.js`
- Markdown rendering via marked.js (CDN)
- BibTeX export (single paper and bulk)
- `summary` field defaults to `summary_zh` for backward compatibility; language toggle only appears when both `summary_zh` and `summary_en` exist

### GitHub Actions (.github/workflows/fetch-papers.yml)

Daily at 00:00 UTC (also manual trigger). Fetches papers, generates `config.js` from `config.toml`, commits changes to `data/`, `feed.xml`, and `config.js` with `github-actions[bot]`, sends email notification with statistics. Only commits if `git diff --staged --quiet` detects changes.

### Supporting Module

`scripts/progress.py` — GitHub Actions-aware progress bar and collapsible group helpers (`github_group`, `github_notice`, `github_warning`). Imported optionally; `main.py` has fallback no-ops when unavailable.

## Key Data Structures

**Paper object** (in `data/papers.json`):
```json
{
  "id": "arxiv_2401.12345",
  "title": "...", "authors": ["..."], "abstract": "...",
  "summary": "Chinese summary (backward compat, = summary_zh)",
  "summary_zh": "Chinese summary (Markdown)",
  "summary_en": "English summary (Markdown)",
  "summary_status": "success | failed",
  "published": "YYYY-MM-DD",
  "source": "arXiv | IACR",
  "url": "...", "pdf_link": "...",
  "keywords": ["..."], "keyword_score": 2,
  "categories": ["cs.CR"],
  "arxiv_id": "2401.12345",
  "iacr_id": "2024/123"
}
```

Paper ID format: `arxiv_{arxiv_id}` or `iacr_{iacr_id}`.

## Configuration

**`config.toml`** is the main configuration file. Key sections:
- `[general]` — `days_back` (retention period), `site_url` (GitHub Pages base URL for RSS), data paths
- `[fetchers.arxiv]` — categories, delay, batch_size, max_results
- `[fetchers.iacr]` — delay
- `[summarizer]` — model, max_tokens, temperature, rate_limit_delay, prompt_template (single-language only; bilingual prompt is in Python)
- `[rss]` — `max_items` (number of papers in RSS feed)
- `[frontend]` — `papers_per_page` (pagination size, default 10)
- `[keywords]` — keyword file path, `apply_to_arxiv`, `apply_to_iacr`

**`keywords.txt`** — Keyword rules. Lines starting with `#` are comments. Each non-empty line is an OR rule; words within a line are AND conditions.

**`scripts/generate_config.py`** — Generates `config.js` from `config.toml` for frontend configuration. Run automatically by GitHub Actions workflow.

## Important Implementation Details

- **API keys**: Code checks both `DASHSCOPE_API_KEY` and `MODELSCOPE_API_KEY` env vars (same service). GitHub Actions uses `MODELSCOPE_API_KEY` secret.
- **arXiv XML validation**: `arxiv.py` checks all required XML elements for `None` before accessing `.text` to handle malformed entries. Maintain this pattern when modifying the fetcher.
- **Rate limits**: arXiv 3s between categories, IACR 2s, DashScope 1s between calls. All configurable in `config.toml`.
- **IACR User-Agent**: The IACR fetcher must send a browser-like `User-Agent` header or the server returns robots.txt instead of RSS.
- **Token budget**: `max_tokens` in config.toml must accommodate both Chinese (~60-70%) and English (~30-40%) summaries.
- **Dependencies**: `requests`, `feedparser`, `python-dateutil`. `tomli` only needed for Python < 3.11 (3.11+ has `tomllib` built-in).
- **GitHub Pages**: `index.html`, `app.js`, `styles.css`, `config.js`, `feed.xml`, and `data/` must remain in the repo root.
- **Frontend config**: `config.js` is auto-generated from `config.toml` by `scripts/generate_config.py` and must be committed to git for GitHub Pages to serve it.
