# Jamie Cui's Personal Homepage

Source for [jamie-cui.github.io](https://jamie-cui.github.io/).

This is a small static personal site with a generated blog index and an integrated research-paper feed at [`/paper-feeds/`](https://jamie-cui.github.io/paper-feeds/).

## Site Structure

- `src/index.org` — Home page source with About and Activities.
- `src/research.org` — Research Interests and Publications page source.
- `src/blogs/` — Blog post sources in Org mode.
- `src/paper-feeds/` — Paper Feeds static frontend, public paper data, and RSS feed source.
- `tools/paper-feeds/` — Paper Feeds fetch/filter/summarize pipeline, configuration, and documentation.
- `imgs/` — Shared images.
- `site.css` — Shared site styling for the personal pages.
- `build.py` — Builds the deployable `_site/` directory.
- `publish.el` — Org-mode HTML fragment export configuration.

## Local Preview

Build the site:

```bash
python3 build.py
```

Serve the generated output:

```bash
cd _site
python3 -m http.server 8000
```

Then open:

- Home: <http://127.0.0.1:8000/>
- Research: <http://127.0.0.1:8000/research/>
- Blogs: <http://127.0.0.1:8000/blogs/>
- Paper Feeds: <http://127.0.0.1:8000/paper-feeds/>

## Paper Feeds

Paper Feeds was merged from the Paper Pulse project and renamed for this site. It fetches, filters, summarizes, and displays recent research papers from arXiv and IACR.

Key files:

- `tools/paper-feeds/config.toml` — pipeline and frontend configuration.
- `tools/paper-feeds/keywords.txt` — keyword filtering rules.
- `src/paper-feeds/data/papers.json` — public paper database used by the frontend.
- `src/paper-feeds/feed.xml` — generated RSS feed.
- `tools/paper-feeds/scripts/main.py` — fetch/filter/summarize pipeline.
- `tools/paper-feeds/scripts/generate_config.py` — generates `src/paper-feeds/config.js`.

See [tools/paper-feeds/README.md](tools/paper-feeds/README.md) for full Paper Feeds documentation.

## GitHub Actions

- `.github/workflows/deploy.yml` builds `_site/` and deploys it to GitHub Pages.
- `.github/workflows/fetch-paper-feeds.yml` runs the Paper Feeds pipeline daily, sends the email report, and commits updated feed data.

Paper Feeds expects these repository secrets:

- `MODELSCOPE_API_KEY` or `DASHSCOPE_API_KEY`
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`
- `EMAIL_TO`

## License

The homepage files are licensed under [CC0-1.0](LICENSE).

The integrated Paper Feeds frontend and tooling are licensed under GPL-3.0; see [src/paper-feeds/LICENSE](src/paper-feeds/LICENSE) and [tools/paper-feeds/LICENSE](tools/paper-feeds/LICENSE).
