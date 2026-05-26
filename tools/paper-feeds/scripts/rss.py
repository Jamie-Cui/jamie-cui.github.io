"""
RSS feed generator for Paper Feeds.

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

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from email.utils import format_datetime


def _date_to_rfc822(date_str: str) -> str:
    """Convert YYYY-MM-DD date string to RFC 822 format for RSS."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return format_datetime(dt)
    except (ValueError, TypeError):
        return format_datetime(datetime.now())


def _paper_text(paper: dict, field: str) -> str:
    value = paper.get(field, "")
    return value.strip() if isinstance(value, str) else ""


def _build_item_description(paper: dict) -> str:
    """Build a readable RSS item body with links and bilingual summaries."""
    url = _paper_text(paper, "url")
    summary_zh = _paper_text(paper, "summary_zh") or _paper_text(paper, "summary")
    summary_en = _paper_text(paper, "summary_en")
    abstract = _paper_text(paper, "abstract")

    sections = []
    if url:
        sections.append(f"Paper Link: {url}")

    if summary_zh:
        sections.append(f"AI Summary (中文):\n{summary_zh}")

    if summary_en:
        sections.append(f"AI Summary (English):\n{summary_en}")

    if abstract:
        sections.append(f"Abstract:\n{abstract}")

    return "\n\n".join(sections)


def generate_rss_feed(
    papers: list,
    output_path: Path,
    site_url: str = "",
    title: str = "Paper Feeds",
    description: str = "Keyword-based research paper feeds from arXiv and IACR",
    max_items: int = 50,
):
    """Generate an RSS 2.0 feed XML file from papers.

    Args:
        papers: List of paper dicts, assumed already sorted by date descending.
        output_path: Path to write the feed.xml file.
        site_url: Base URL of the site (e.g. "https://user.github.io/paper-feeds").
        title: Feed title.
        description: Feed description.
        max_items: Maximum number of items to include in the feed.
    """
    ET.register_namespace("atom", "http://www.w3.org/2005/Atom")
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = site_url or "https://github.com"
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.now())

    if site_url:
        feed_url = site_url.rstrip("/") + "/feed.xml"
        atom_link = ET.SubElement(
            channel,
            "{http://www.w3.org/2005/Atom}link",
            href=feed_url,
            rel="self",
            type="application/rss+xml",
        )

    for paper in papers[:max_items]:
        item = ET.SubElement(channel, "item")

        ET.SubElement(item, "title").text = paper.get("title", "Untitled")
        ET.SubElement(item, "link").text = paper.get("url", "")
        ET.SubElement(item, "guid", isPermaLink="true").text = paper.get("url", "")

        ET.SubElement(item, "description").text = _build_item_description(paper)

        pub_date = paper.get("published", "")
        if pub_date:
            ET.SubElement(item, "pubDate").text = _date_to_rfc822(pub_date)

        # Source as category
        source = paper.get("source")
        if source:
            ET.SubElement(item, "category").text = source

        # Keywords as categories
        for kw in paper.get("keywords", [])[:5]:
            ET.SubElement(item, "category").text = kw

    # Write XML with declaration
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

    print(f"✓ Generated RSS feed at {output_path} ({min(len(papers), max_items)} items)")
