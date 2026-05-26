#!/usr/bin/env python3
"""
Main script for fetching, filtering, and summarizing papers from arXiv and IACR.

Copyright (C) 2024-2026 Paper Pulse Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = TOOL_DIR.parent.parent
PUBLIC_DIR = REPO_ROOT / "src" / "paper-feeds"
REPORTS_DIR = TOOL_DIR / "reports"

# Add scripts directory to path
sys.path.insert(0, str(TOOL_DIR / "scripts"))

from fetchers.arxiv import ArxivFetcher
from fetchers.iacr import IACRFetcher
from filter import KeywordFilter
from summarizer import ModelScopeSummarizer
from rss import generate_rss_feed

# Load TOML config (Python 3.11+ has tomllib built-in)
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Import progress utilities
try:
    from progress import github_group, github_notice, github_warning, ProgressBar

    HAS_PROGRESS = True
except ImportError:
    HAS_PROGRESS = False

    # Fallback no-op context manager
    class github_group:
        def __init__(self, name):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    def github_notice(msg):
        print(f"Notice: {msg}")

    def github_warning(msg):
        print(f"Warning: {msg}")


def _wrap_text(text: str, width: int = 72) -> str:
    """Wrap text to given width, preserving existing line breaks."""
    import textwrap

    result_lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            result_lines.append("")
        else:
            result_lines.extend(textwrap.wrap(paragraph, width=width))
    return "\n".join(result_lines)


def generate_email_report(
    new_papers: list,
    retry_papers: list,
    failed_papers: list,
    total_count: int,
    usage_stats: dict,
    output_path: Path,
    site_url: str,
    summary_language: str = "zh",
):
    """Generate a plain-text email report with paper details and summaries.

    Args:
        summary_language: Which summary to include in the email.
            "zh" = Chinese only, "en" = English only, "both" = both.
    """
    lines = []
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    sep = "=" * 40

    lines.append(sep)
    lines.append("Paper Feeds Daily Report")
    lines.append(sep)
    lines.append(f"Date: {date_str}")
    lines.append("")

    # Statistics
    lines.append("STATISTICS")
    lines.append("-" * 40)
    lines.append(f"  New papers fetched:       {len(new_papers)}")
    lines.append(f"  Retry summaries:          {len(retry_papers)}")
    lines.append(f"  Failed summaries:         {len(failed_papers)}")
    lines.append(f"  Total papers in database: {total_count}")
    lines.append("")

    lines.append("AI TOKEN USAGE")
    lines.append("-" * 40)
    lines.append(f"  Input tokens:  {usage_stats['input_tokens']}")
    lines.append(f"  Output tokens: {usage_stats['output_tokens']}")
    lines.append(f"  Total tokens:  {usage_stats['total_tokens']}")
    lines.append("")

    # New papers section
    all_report_papers = new_papers + retry_papers
    if all_report_papers:
        lines.append(sep)
        lines.append(f"NEW PAPERS ({len(all_report_papers)})")
        lines.append(sep)
        lines.append("")

        for i, paper in enumerate(all_report_papers, 1):
            title = paper.get("title", "Untitled")
            url = paper.get("url", "")
            source = paper.get("source", "Unknown")
            published = paper.get("published", "Unknown")
            keywords = paper.get("keywords", [])
            summary_zh = paper.get("summary_zh", "")
            summary_en = paper.get("summary_en", "")

            lines.append(f"[{i}] {title}")
            lines.append(f"    URL:       {url}")
            lines.append(f"    Source:    {source}")
            lines.append(f"    Published: {published}")
            if keywords:
                lines.append(f"    Keywords:  {', '.join(keywords)}")
            lines.append("")

            has_summary = False

            if summary_language in ("zh", "both") and summary_zh:
                if summary_language == "both":
                    lines.append("    -- Chinese Summary --")
                lines.append("")
                lines.append(_wrap_text(summary_zh))
                lines.append("")
                has_summary = True

            if summary_language in ("en", "both") and summary_en:
                if summary_language == "both":
                    lines.append("    -- English Summary --")
                lines.append("")
                lines.append(_wrap_text(summary_en))
                lines.append("")
                has_summary = True

            if not has_summary:
                abstract = paper.get("abstract", "No summary available.")
                lines.append("    -- Abstract --")
                lines.append("")
                lines.append(_wrap_text(abstract))
                lines.append("")

            lines.append("-" * 40)
            lines.append("")
    else:
        lines.append("No new papers in this run.")
        lines.append("")

    # Links
    if site_url:
        lines.append("LINKS")
        lines.append("-" * 40)
        lines.append(f"  View Papers: {site_url}")
        lines.append("")

    lines.append(sep)
    lines.append("This is an automated report from Paper Feeds.")
    lines.append("Powered by arXiv, IACR ePrint, and DashScope (Qwen).")
    lines.append(sep)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ Generated email report at {output_path}")


def load_existing_data(filepath: Path) -> dict:
    """Load existing papers data."""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"papers": [], "last_updated": None}


def save_data(filepath: Path, data: dict):
    """Save papers data to JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved data to {filepath}")


def remove_old_papers(papers: list, days: int = 7) -> list:
    """Remove papers older than specified days."""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []

    for paper in papers:
        try:
            paper_date = datetime.strptime(paper["published"], "%Y-%m-%d")
            if paper_date >= cutoff:
                filtered.append(paper)
        except (ValueError, KeyError):
            filtered.append(paper)

    removed = len(papers) - len(filtered)
    if removed > 0:
        print(f"✓ Removed {removed} papers older than {days} days")

    return filtered


def merge_papers(existing: list, new: list) -> list:
    """Merge new papers with existing, avoiding duplicates and updating with new data."""
    existing_dict = {p["id"]: p for p in existing}

    new_count = 0
    updated_count = 0
    for paper in new:
        if paper["id"] not in existing_dict:
            existing_dict[paper["id"]] = paper
            new_count += 1
        else:
            if paper.get("summary_status") == "success":
                existing_dict[paper["id"]] = paper
                updated_count += 1

    print(f"✓ Added {new_count} new papers, updated {updated_count} papers")
    return list(existing_dict.values())


def retry_failed_summaries(
    failed_papers: list, summarizer: ModelScopeSummarizer
) -> tuple:
    """Retry summarization for failed papers."""
    if not failed_papers:
        return [], []

    print(f"\nRetrying {len(failed_papers)} previously failed papers...")
    return summarizer.batch_summarize(failed_papers)


def load_config() -> dict:
    """Load configuration from config.toml."""
    config_path = TOOL_DIR / "config.toml"

    if config_path.exists():
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    else:
        print(f"⚠️  Config file not found at {config_path}, using defaults")
        return {}


def main():
    """Main execution function."""
    print("=" * 70)
    print("📚 Paper Feeds - Starting")
    print("=" * 70)

    # Load configuration
    config = load_config()

    # Configuration with defaults
    DAYS_BACK = config.get("general", {}).get("days_back", 7)
    DATA_DIR = PUBLIC_DIR / config.get("general", {}).get("data_dir", "data")
    PAPERS_FILE = DATA_DIR / config.get("general", {}).get("papers_file", "papers.json")
    FAILED_FILE = REPORTS_DIR / config.get("general", {}).get("failed_file", "failed.json")

    # Get API key from environment
    api_key = os.getenv("MODELSCOPE_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print(
            "::error::API key not set. Please set DASHSCOPE_API_KEY in GitHub Secrets"
        )
        print("Get your API key from: https://dashscope.console.aliyun.com/")
        sys.exit(1)

    # Initialize components
    with github_group("🔧 Initializing components"):
        print("Creating fetchers and filter...")

        # Get fetcher configs
        arxiv_config = config.get("fetchers", {}).get("arxiv", {})
        iacr_config = config.get("fetchers", {}).get("iacr", {})

        arxiv_fetcher = ArxivFetcher(
            days_back=DAYS_BACK,
            delay=arxiv_config.get("delay", 3.0),
            categories=arxiv_config.get("categories"),
            batch_size=arxiv_config.get("batch_size"),
            max_results=arxiv_config.get("max_results"),
        )
        iacr_fetcher = IACRFetcher(
            days_back=DAYS_BACK, delay=iacr_config.get("delay", 2.0)
        )

        # Get keyword filter config
        keywords_config = config.get("keywords", {})
        keywords_file = keywords_config.get("file")
        if keywords_file:
            keywords_file = TOOL_DIR / keywords_file
        keyword_filter = KeywordFilter(config_file=keywords_file)

        # Get summarizer config
        summarizer_config = config.get("summarizer", {})
        summarizer = ModelScopeSummarizer(
            api_key=api_key,
            model=summarizer_config.get("model"),
            max_tokens=summarizer_config.get("max_tokens"),
            temperature=summarizer_config.get("temperature"),
            timeout=summarizer_config.get("timeout"),
            rate_limit_delay=summarizer_config.get("rate_limit_delay"),
            max_retries=summarizer_config.get("max_retries", 3),
            retry_delay=summarizer_config.get("retry_delay", 5.0),
            prompt_template=summarizer_config.get("prompt_template"),
        )
        print("✓ All components initialized")

    # Load existing data
    with github_group("💾 Loading existing data"):
        existing_data = load_existing_data(PAPERS_FILE)
        existing_failed = load_existing_data(FAILED_FILE)
        print(f"✓ Loaded {len(existing_data.get('papers', []))} existing papers")
        print(f"✓ Loaded {len(existing_failed.get('papers', []))} failed papers")

    # Retry previously failed papers
    retry_successful = []
    retry_failed = []
    if existing_failed.get("papers"):
        with github_group("🔄 Retrying failed summaries"):
            retry_successful, retry_failed = retry_failed_summaries(
                existing_failed["papers"], summarizer
            )
            if retry_successful:
                github_notice(
                    f"Successfully summarized {len(retry_successful)} previously failed papers"
                )

    # Fetch papers from sources
    with github_group("📥 Fetching papers from sources"):
        print("Fetching from arXiv...")
        arxiv_papers = arxiv_fetcher.fetch_papers()

        print("\nFetching from IACR...")
        iacr_papers = iacr_fetcher.fetch_papers()

        all_fetched = arxiv_papers + iacr_papers
        print(f"\n✓ Total fetched: {len(all_fetched)} papers")
        print(f"  - arXiv: {len(arxiv_papers)} papers")
        print(f"  - IACR: {len(iacr_papers)} papers")

    # Filter by keywords with source-specific control
    with github_group("🔍 Filtering by keywords"):
        keywords_config = config.get("keywords", {})
        apply_to_arxiv = keywords_config.get("apply_to_arxiv", True)
        apply_to_iacr = keywords_config.get("apply_to_iacr", True)

        # Separate papers by source
        arxiv_papers_to_filter = [p for p in all_fetched if p.get("source") == "arXiv"]
        iacr_papers_to_filter = [p for p in all_fetched if p.get("source") == "IACR"]

        filtered_papers = []

        # Apply filtering based on configuration
        if apply_to_arxiv:
            print(
                f"Applying keyword filter to arXiv papers ({len(arxiv_papers_to_filter)} papers)..."
            )
            filtered_arxiv = keyword_filter.filter_papers(arxiv_papers_to_filter)
            filtered_papers.extend(filtered_arxiv)
            print(f"  Matched {len(filtered_arxiv)} arXiv papers")
        else:
            print(
                f"Skipping keyword filter for arXiv (fetching all {len(arxiv_papers_to_filter)} papers)"
            )
            filtered_papers.extend(arxiv_papers_to_filter)

        if apply_to_iacr:
            print(
                f"Applying keyword filter to IACR papers ({len(iacr_papers_to_filter)} papers)..."
            )
            filtered_iacr = keyword_filter.filter_papers(iacr_papers_to_filter)
            filtered_papers.extend(filtered_iacr)
            print(f"  Matched {len(filtered_iacr)} IACR papers")
        else:
            print(
                f"Skipping keyword filter for IACR (fetching all {len(iacr_papers_to_filter)} papers)"
            )
            filtered_papers.extend(iacr_papers_to_filter)

        print(f"\n✓ Total papers after filtering: {len(filtered_papers)}")
        if filtered_papers:
            github_notice(
                f"Selected {len(filtered_papers)} papers (arXiv filter: {apply_to_arxiv}, IACR filter: {apply_to_iacr})"
            )
        else:
            github_warning("No papers selected")

    # Separate new papers from cached ones (to avoid re-summarizing)
    with github_group("📋 Checking cache"):
        existing_dict = {p["id"]: p for p in existing_data.get("papers", [])}
        new_papers = []
        cached_papers = []

        for paper in filtered_papers:
            if paper["id"] in existing_dict:
                # Paper already exists, reuse cached summary
                cached_papers.append(existing_dict[paper["id"]])
            else:
                # New paper, needs summarization
                new_papers.append(paper)

        print(f"✓ Found {len(new_papers)} new papers (need summarization)")
        print(f"✓ Reusing {len(cached_papers)} cached summaries")

    # Summarize only new papers
    with github_group("🤖 Generating AI summaries"):
        if new_papers:
            successful, failed = summarizer.batch_summarize(new_papers)
        else:
            successful, failed = [], []

        new_summary_count = len(successful)
        newly_summarized = list(successful)  # save before combining with cache

        # Combine newly summarized papers with cached ones
        successful = successful + cached_papers

    # Combine with retry results
    all_successful = successful + retry_successful

    all_failed = failed + retry_failed

    if not all_successful:
        print("\n⚠️  No new papers to add")
        existing_data["last_updated"] = datetime.now().isoformat()
        save_data(PAPERS_FILE, existing_data)
        if all_failed:
            failed_data = {
                "papers": all_failed,
                "last_updated": datetime.now().isoformat(),
                "count": len(all_failed),
            }
            save_data(FAILED_FILE, failed_data)
        # Still generate email report (even with no new papers)
        usage_stats = summarizer.get_usage_stats()
        site_url = config.get("general", {}).get("site_url", "")
        summary_language = config.get("email", {}).get("summary_language", "zh")
        email_report_path = REPORTS_DIR / "email_report.txt"
        generate_email_report(
            new_papers=[],
            retry_papers=[],
            failed_papers=all_failed,
            total_count=len(existing_data.get("papers", [])),
            usage_stats=usage_stats,
            output_path=email_report_path,
            site_url=site_url,
            summary_language=summary_language,
        )
        return

    # Merge with existing papers
    with github_group("📦 Merging with existing data"):
        all_papers = merge_papers(existing_data.get("papers", []), all_successful)
        all_papers = remove_old_papers(all_papers, days=DAYS_BACK)
        all_papers.sort(key=lambda p: p.get("published", "0000-00-00"), reverse=True)

    # Save data
    with github_group("💾 Saving data"):
        papers_data = {
            "papers": all_papers,
            "last_updated": datetime.now().isoformat(),
            "total_count": len(all_papers),
        }
        save_data(PAPERS_FILE, papers_data)

        # Generate RSS feed
        rss_config = config.get("rss", {})
        site_url = config.get("general", {}).get("site_url", "")
        feed_path = PUBLIC_DIR / "feed.xml"
        generate_rss_feed(
            papers=all_papers,
            output_path=feed_path,
            site_url=site_url,
            title="Paper Feeds",
            description="Keyword-based research paper feeds from arXiv and IACR",
            max_items=rss_config.get("max_items", 50),
        )

        source_feeds = [
            ("arXiv", "feed-arxiv.xml", "Paper Feeds (arXiv)"),
            ("IACR", "feed-iacr.xml", "Paper Feeds (IACR)"),
        ]
        for source, filename, feed_title in source_feeds:
            source_papers = [p for p in all_papers if p.get("source") == source]
            generate_rss_feed(
                papers=source_papers,
                output_path=PUBLIC_DIR / filename,
                site_url=site_url,
                title=feed_title,
                description=f"Keyword-based research paper feeds from {source}",
                max_items=rss_config.get("max_items", 50),
            )

        if all_failed:
            failed_data = {
                "papers": all_failed,
                "last_updated": datetime.now().isoformat(),
                "count": len(all_failed),
            }
            save_data(FAILED_FILE, failed_data)
        elif FAILED_FILE.exists():
            FAILED_FILE.unlink()
            print("✓ Cleared failed papers file (all succeeded)")

    # Get token usage statistics
    usage_stats = summarizer.get_usage_stats()

    # Summary
    print("\n" + "=" * 70)
    print("✅ Paper Feeds - Complete")
    print("=" * 70)
    print(f"📊 Statistics:")
    print(f"  Total papers in database: {len(all_papers)}")
    print(f"  New summaries: {new_summary_count}")
    print(f"  Retry summaries: {len(retry_successful)}")
    print(f"  Failed summaries: {len(all_failed)}")
    print(f"  Last updated: {papers_data['last_updated']}")
    print(f"\n🤖 Token Usage:")
    print(f"  Input tokens: {usage_stats['input_tokens']}")
    print(f"  Output tokens: {usage_stats['output_tokens']}")
    print(f"  Total tokens: {usage_stats['total_tokens']}")
    print("=" * 70)

    # Output statistics for GitHub Actions to capture
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"new_papers={new_summary_count}\n")
            f.write(f"retry_papers={len(retry_successful)}\n")
            f.write(f"failed_papers={len(all_failed)}\n")
            f.write(f"total_papers={len(all_papers)}\n")
            f.write(f"input_tokens={usage_stats['input_tokens']}\n")
            f.write(f"output_tokens={usage_stats['output_tokens']}\n")
            f.write(f"total_tokens={usage_stats['total_tokens']}\n")

    github_notice(f"Successfully updated {len(all_papers)} papers")

    # Generate email report with paper details
    site_url = config.get("general", {}).get("site_url", "")
    summary_language = config.get("email", {}).get("summary_language", "zh")
    email_report_path = REPORTS_DIR / "email_report.txt"
    generate_email_report(
        new_papers=newly_summarized,
        retry_papers=retry_successful,
        failed_papers=all_failed,
        total_count=len(all_papers),
        usage_stats=usage_stats,
        output_path=email_report_path,
        site_url=site_url,
        summary_language=summary_language,
    )


if __name__ == "__main__":
    main()
