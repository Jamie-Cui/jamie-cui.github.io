# Jamie Cui's Personal Homepage

Source for [jamie-cui.github.io](https://jamie-cui.github.io/).

This is a small static personal site with a generated blog index and an integrated research-paper feed at [`/paper-feeds/`](https://jamie-cui.github.io/paper-feeds/).

## Site Structure

- `index.html` — Home page with About, Research Interests, and Activities.
- `publications/` — Publications page.
- `blogs/` — Blog index template plus `.org` source posts.
- `paper-feeds/` — Integrated Paper Feeds app, data pipeline, RSS feed, and frontend.
- `imgs/` — Shared images.
- `site.css` — Shared site styling for the personal pages.
- `build.py` — Builds the deployable `_site/` directory.
- `publish.el` — Org-mode HTML export configuration for blog posts.

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
- Publications: <http://127.0.0.1:8000/publications/>
- Blogs: <http://127.0.0.1:8000/blogs/>
- Paper Feeds: <http://127.0.0.1:8000/paper-feeds/>

## Paper Feeds

`paper-feeds/` was merged from the Paper Pulse project and renamed for this site. It fetches, filters, summarizes, and displays recent research papers from arXiv and IACR.

Key files:

- `paper-feeds/config.toml` — pipeline and frontend configuration.
- `paper-feeds/keywords.txt` — keyword filtering rules.
- `paper-feeds/data/papers.json` — paper database used by the frontend.
- `paper-feeds/feed.xml` — generated RSS feed.
- `paper-feeds/scripts/main.py` — fetch/filter/summarize pipeline.
- `paper-feeds/scripts/generate_config.py` — generates `paper-feeds/config.js`.

See [paper-feeds/README.md](paper-feeds/README.md) for full Paper Feeds documentation.

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

The integrated Paper Feeds app under `paper-feeds/` is licensed under [GPL-3.0](paper-feeds/LICENSE).
