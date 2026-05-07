# Setup Guide

This guide will help you set up and deploy Paper Feeds on GitHub Pages.

## Prerequisites

- GitHub account
- DashScope API key (free tier available at https://dashscope.console.aliyun.com/)
- Git installed locally

## Step 1: Repository Setup

1. Push this code to your GitHub repository:
   ```bash
   git add .
   git commit -m "Initial commit: Paper Feeds"
   git push origin master
   ```

## Step 2: Configure GitHub Secrets

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:
   - Name: `DASHSCOPE_API_KEY` (or `MODELSCOPE_API_KEY`)
   - Value: Your DashScope/ModelScope API key

## Step 3: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If prompted, click **I understand my workflows, go ahead and enable them**
3. The workflow should now be enabled

## Step 4: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - Source: **Deploy from a branch**
   - Branch: **master** (or **main** if that's your default branch)
   - Folder: **/ (root)**
3. Click **Save**
4. Wait a few minutes for the site to deploy
5. Your site will be available at: `https://<username>.github.io/<repo-name>/`

## Step 5: First Run

### Option A: Manual Trigger (Recommended for first run)

1. Go to **Actions** tab
2. Click on **Fetch Papers** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for the workflow to complete (5-10 minutes depending on number of papers)

### Option B: Wait for Automatic Run

The workflow runs automatically every day at 00:00 UTC.

## Step 6: Verify

1. After the workflow completes, check that `src/paper-feeds/data/papers.json` has been created
2. Visit your GitHub Pages URL
3. You should see the papers displayed in card format with bilingual summaries

## Troubleshooting

### Workflow fails with "API key not set"
- Make sure you've added the secret in Step 2
- The secret name must be `DASHSCOPE_API_KEY` or `MODELSCOPE_API_KEY`

### No papers showing up
- Check the workflow logs to see if papers were fetched
- Papers must match your keyword filters in `keywords.txt`
- Only papers from the configured time period are kept (default: 7 days)

### GitHub Pages shows 404
- Make sure you selected `/ (root)` as the folder in Pages settings
- Wait a few minutes after enabling Pages for DNS to propagate
- Check that `src/paper-feeds/index.html` exists in your repository

### Rate limiting issues
- The default delays (3s for arXiv, 1s for summarization) should prevent rate limiting
- If you still hit limits, increase delays in `config.toml`

## Customization

### Change keyword filters

Edit `tools/paper-feeds/keywords.txt` to customize which papers are included.

**Format:**
- Each line is an OR condition
- Multiple words on the same line use AND logic (all must match)
- Lines starting with `#` are comments
- Empty lines are ignored

**Examples:**
```
# Match papers with "transformer" OR "attention"
transformer
attention

# Match papers with BOTH "neural" AND "backdoor" (both words must appear)
neural backdoor

# Match papers with "federated learning" (phrase)
federated learning
```

A paper will be included if it matches ANY line in the file.

### Change configuration settings

Edit `config.toml` to customize:

**Retention period:**
```toml
[general]
days_back = 7  # Keep papers from last 7 days
```

**arXiv categories:**
```toml
[fetchers.arxiv]
categories = ["cs.CR", "cs.AI", "cs.LG", "cs.CL"]  # Customize categories
```

**AI model:**
```toml
[summarizer]
model = "qwen-plus"  # Options: qwen-turbo, qwen-plus, qwen-max
max_tokens = 1500     # For bilingual summaries
```

**Rate limits:**
```toml
[fetchers.arxiv]
delay = 3.0  # Delay between arXiv requests

[summarizer]
rate_limit_delay = 1.0  # Delay between summarization calls
```

See `CONFIG_GUIDE.md` for more detailed configuration options.

### Change workflow schedule

Edit `.github/workflows/fetch-papers.yml`, line 5:
```yaml
- cron: '0 0 * * *'  # Daily at 00:00 UTC
```

Use [crontab.guru](https://crontab.guru/) to generate different schedules.

## Manual Local Testing

Test the fetcher locally before deploying:

```bash
# Install dependencies
pip install -r tools/paper-feeds/requirements.txt

# Set API key
export DASHSCOPE_API_KEY="your-key-here"

# Run the script
python tools/paper-feeds/scripts/main.py
```

This will update `src/paper-feeds/data/papers.json` and `src/paper-feeds/feed.xml`. Run `python3 build.py`, then serve `_site/` to view the results.

## License

MIT
