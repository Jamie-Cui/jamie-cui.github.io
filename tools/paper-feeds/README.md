# Paper Feeds

**Automatically fetch, filter, and summarize research papers from arXiv & IACR — with AI-generated bilingual (Chinese/English) summaries. Deployed for free on GitHub Pages, updated daily via GitHub Actions.**

[Live Demo](https://jamie-cui.github.io/paper-feeds/) | [RSS Feed](https://jamie-cui.github.io/paper-feeds/feed.xml) | [中文文档](README_CN.md)

![Paper Feeds Screenshot](docs/screenshot.png)

## Why Paper Feeds?

- Tired of manually checking arXiv every day? Paper Feeds fetches papers automatically.
- Only care about specific topics? Flexible keyword filtering (AND/OR logic) keeps only what matters.
- Need Chinese + English summaries? AI generates both — toggle per card with one click.
- Don't want to pay for hosting? Runs entirely on GitHub Actions + Pages. Zero cost.

## Features

| Feature | Description |
|---|---|
| **Multi-source** | Fetches from arXiv (configurable categories) and IACR ePrint |
| **Keyword filtering** | OR between lines, AND within a line — fine-grained control |
| **Bilingual AI summaries** | Chinese + English via Qwen (DashScope API), toggle per card |
| **Daily automation** | GitHub Actions cron job, auto-commits results |
| **RSS feed** | Subscribe in any reader — `feed.xml` auto-generated |
| **BibTeX export** | Single paper or bulk export |
| **Email digest** | Daily report with stats and token usage |
| **Static site** | No server needed — GitHub Pages serves everything |
| **Markdown summaries** | Rich formatting in AI-generated summaries |

## Quick Start (5 steps)

### 1. Use this template / Fork

Click **"Use this template"** (or fork) to create your own copy.

### 2. Get a DashScope API key

Sign up at [DashScope Console](https://dashscope.console.aliyun.com/) — free tier available.

### 3. Add your API key to GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**:
- Name: `MODELSCOPE_API_KEY` (or `DASHSCOPE_API_KEY`)
- Value: your API key

### 4. Enable GitHub Pages

Go to **Settings → Pages**:
- Source: **Deploy from a branch**
- Branch: `master`, Folder: `/ (root)`

### 5. Run the workflow

Go to **Actions → Fetch Papers → Run workflow**. After it completes, visit `https://<username>.github.io/<repo-name>/`.

From now on, papers are fetched automatically every day at 00:00 UTC.

### 6. (Optional) Enable email digest

Paper Feeds can send a daily email report with statistics (new papers, failed summaries, token usage). To enable it, add three more secrets in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `EMAIL_USERNAME` | Gmail address used to send the report (e.g. `you@gmail.com`) |
| `EMAIL_PASSWORD` | Gmail [App Password](https://myaccount.google.com/apppasswords) (not your login password) |
| `EMAIL_TO` | Recipient address (can be the same as `EMAIL_USERNAME`) |

> **Note:** Gmail requires an **App Password** — you must enable 2-Step Verification on your Google account first, then generate an App Password under [Security → App passwords](https://myaccount.google.com/apppasswords). Regular Gmail passwords will not work.

If these secrets are not set, the workflow still runs normally — the email step is simply skipped.

## Customization

### Keywords (`keywords.txt`)

```
# Each line = OR condition. Words on same line = AND condition.
transformer              # Papers containing "transformer"
neural backdoor          # Papers containing BOTH "neural" AND "backdoor"
federated learning       # Papers containing "federated learning"
```

Keyword filtering can be independently toggled per source (`apply_to_arxiv` / `apply_to_iacr` in `config.toml`).

### Configuration (`config.toml`)

| Setting | Where | Default |
|---|---|---|
| Paper retention | `general.days_back` | 30 days |
| Papers per page | `frontend.papers_per_page` | 10 |
| arXiv categories | `fetchers.arxiv.categories` | cs.CR, cs.AI, cs.LG, cs.CL |
| AI model | `summarizer.model` | qwen-plus |
| RSS items | `rss.max_items` | 50 |
| Site URL | `general.site_url` | *(your GitHub Pages URL)* |

See [CONFIG_GUIDE.md](CONFIG_GUIDE.md) for all options.

## Project Structure

```
.
├── .github/workflows/
│   └── fetch-paper-feeds.yml # Daily automation
├── tools/paper-feeds/
│   ├── scripts/
│   │   ├── fetchers/
│   │   │   ├── arxiv.py      # arXiv API fetcher
│   │   │   └── iacr.py       # IACR RSS fetcher
│   │   ├── filter.py         # Keyword filtering engine
│   │   ├── summarizer.py     # Bilingual AI summarization
│   │   ├── rss.py            # RSS feed generator
│   │   ├── generate_config.py # Frontend config generator
│   │   └── main.py           # Pipeline orchestrator
│   ├── reports/
│   │   └── failed.json       # Failed summarization queue
│   ├── config.toml           # All configuration
│   └── keywords.txt          # Keyword filter rules
└── src/paper-feeds/
    ├── data/
    │   └── papers.json       # Paper database
    ├── index.html / app.js / styles.css  # Frontend
    ├── config.js             # Frontend config (auto-generated)
    └── feed.xml              # RSS feed (auto-generated)
```

## How It Works

```
Fetch (arXiv + IACR)
  → Filter (keyword matching)
    → Summarize (Qwen AI, bilingual)
      → Merge & Deduplicate
        → Save (papers.json)
          → Generate RSS (feed.xml)
            → Commit & Push (GitHub Actions)
```

Failed summaries are retried automatically on the next run.

## License

[GPL-3.0](LICENSE)
