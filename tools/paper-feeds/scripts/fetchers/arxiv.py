"""
arXiv paper fetcher for Paper Feeds.

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

import requests
import time
from datetime import datetime, timedelta, timezone
from typing import List, Dict
import xml.etree.ElementTree as ET


class ArxivFetcher:
    """Fetches papers from arXiv API."""

    BASE_URL = "http://export.arxiv.org/api/query"
    DEFAULT_CATEGORIES = [
        "cs.CR",
        "cs.AI",
        "cs.LG",
        "cs.CL",
    ]  # Cryptography, AI, ML, Computation and Language
    DEFAULT_BATCH_SIZE = 100
    DEFAULT_MAX_RESULTS = 500

    def __init__(
        self,
        days_back: int = 7,
        delay: float = 3.0,
        categories: List[str] = None,
        batch_size: int = None,
        max_results: int = None,
    ):
        """
        Initialize arXiv fetcher.

        Args:
            days_back: Number of days to look back for papers
            delay: Delay between requests to respect rate limits (arXiv asks for 3 seconds)
            categories: List of arXiv categories to fetch (default: cs.CR, cs.AI, cs.LG, cs.CL)
            batch_size: Number of results per request
            max_results: Maximum total results per category
        """
        self.days_back = days_back
        self.delay = delay
        self.categories = categories or self.DEFAULT_CATEGORIES
        self.batch_size = batch_size or self.DEFAULT_BATCH_SIZE
        self.max_results = max_results or self.DEFAULT_MAX_RESULTS

    def fetch_papers(self) -> List[Dict]:
        """
        Fetch recent papers from arXiv.

        Returns:
            List of paper dictionaries with metadata
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.days_back)
        all_papers = []

        for category in self.categories:
            print(f"Fetching from arXiv category: {category}")
            papers = self._fetch_category(category, cutoff_date)
            all_papers.extend(papers)
            time.sleep(self.delay)

        # Remove duplicates (papers can appear in multiple categories)
        seen_ids = set()
        unique_papers = []
        for paper in all_papers:
            if paper["id"] not in seen_ids:
                seen_ids.add(paper["id"])
                unique_papers.append(paper)

        print(f"Fetched {len(unique_papers)} unique papers from arXiv")
        return unique_papers

    def _fetch_category(self, category: str, cutoff_date: datetime) -> List[Dict]:
        """
        Fetch papers from a specific arXiv category.

        Args:
            category: arXiv category (e.g., 'cs.CR')
            cutoff_date: Only fetch papers after this date

        Returns:
            List of paper dictionaries
        """
        papers = []
        start = 0

        while True:
            params = {
                "search_query": f"cat:{category}",
                "start": start,
                "max_results": self.batch_size,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }

            try:
                response = requests.get(self.BASE_URL, params=params, timeout=30)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching from arXiv category {category}: {e}")
                break

            # Parse XML response
            root = ET.fromstring(response.content)
            namespace = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom",
            }

            entries = root.findall("atom:entry", namespace)

            if not entries:
                break

            for entry in entries:
                # Extract required fields with null checks
                published_elem = entry.find("atom:published", namespace)
                id_elem = entry.find("atom:id", namespace)
                title_elem = entry.find("atom:title", namespace)
                abstract_elem = entry.find("atom:summary", namespace)

                # Skip malformed entries
                if not all(
                    [
                        published_elem is not None,
                        id_elem is not None,
                        title_elem is not None,
                        abstract_elem is not None,
                    ]
                ):
                    print(f"Skipping malformed entry (missing required fields)")
                    continue

                try:
                    published = published_elem.text
                    published_date = datetime.fromisoformat(
                        published.replace("Z", "+00:00")
                    )

                    # Stop if we've gone past the cutoff date
                    if published_date < cutoff_date:
                        return papers

                    # Extract paper metadata
                    paper_id = id_elem.text.split("/abs/")[-1]
                    title = title_elem.text.strip().replace("\n", " ")
                    abstract = abstract_elem.text.strip().replace("\n", " ")

                    authors = []
                    for author in entry.findall("atom:author", namespace):
                        name_elem = author.find("atom:name", namespace)
                        if name_elem is not None and name_elem.text:
                            authors.append(name_elem.text)

                    pdf_link = None
                    for link in entry.findall("atom:link", namespace):
                        if link.get("title") == "pdf":
                            pdf_link = link.get("href")
                            break

                    # Get categories
                    categories = []
                    primary_category = entry.find("arxiv:primary_category", namespace)
                    if primary_category is not None:
                        term = primary_category.get("term")
                        if term:
                            categories.append(term)

                    for cat in entry.findall("atom:category", namespace):
                        term = cat.get("term")
                        if term and term not in categories:
                            categories.append(term)

                    papers.append(
                        {
                            "id": f"arxiv_{paper_id}",
                            "arxiv_id": paper_id,
                            "title": title,
                            "authors": authors,
                            "abstract": abstract,
                            "published": published_date.strftime("%Y-%m-%d"),
                            "source": "arXiv",
                            "pdf_link": pdf_link,
                            "url": f"https://arxiv.org/abs/{paper_id}",
                            "categories": categories,
                            "published_official": True,
                        }
                    )
                except (AttributeError, ValueError) as e:
                    print(f"Error parsing entry: {e}")
                    continue

            start += self.batch_size

            # Limit to avoid excessive requests
            if start >= self.max_results:
                break

        return papers
