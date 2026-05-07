"""
IACR ePrint paper fetcher for Paper Feeds.

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
import feedparser
import time
from datetime import datetime, timedelta
from typing import List, Dict


class IACRFetcher:
    """Fetches papers from IACR ePrint archive."""

    RSS_URL = "https://eprint.iacr.org/rss/rss.xml"

    def __init__(self, days_back: int = 7, delay: float = 2.0):
        """
        Initialize IACR fetcher.

        Args:
            days_back: Number of days to look back for papers
            delay: Delay between requests to respect rate limits
        """
        self.days_back = days_back
        self.delay = delay

    def fetch_papers(self) -> List[Dict]:
        """
        Fetch recent papers from IACR ePrint.

        Returns:
            List of paper dictionaries with metadata
        """
        cutoff_date = datetime.now() - timedelta(days=self.days_back)
        papers = []

        print("Fetching from IACR ePrint archive")

        try:
            # Fetch RSS feed (User-Agent required; server returns robots.txt otherwise)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            }
            response = requests.get(self.RSS_URL, timeout=30, headers=headers)
            response.raise_for_status()

            # Parse RSS feed
            feed = feedparser.parse(response.content)

            for entry in feed.entries:
                # Parse publication date
                if hasattr(entry, 'published_parsed'):
                    published_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    published_date = datetime(*entry.updated_parsed[:6])
                else:
                    continue

                # Skip if older than cutoff
                if published_date < cutoff_date:
                    continue

                # Extract paper ID from link (e.g., https://eprint.iacr.org/2024/123)
                paper_id = entry.link.split('/')[-1]

                # Extract title
                title = entry.title.strip()

                # Extract authors from description or title
                # IACR RSS format: "Title by Author1, Author2"
                authors = []
                if hasattr(entry, 'author'):
                    authors = [a.strip() for a in entry.author.split(',')]
                elif ' by ' in title:
                    parts = title.split(' by ')
                    if len(parts) == 2:
                        title = parts[0].strip()
                        authors = [a.strip() for a in parts[1].split(',')]

                # Extract abstract/summary
                abstract = ""
                if hasattr(entry, 'summary'):
                    abstract = entry.summary.strip()
                elif hasattr(entry, 'description'):
                    abstract = entry.description.strip()

                # Construct PDF link
                pdf_link = f"https://eprint.iacr.org/{paper_id}.pdf"

                papers.append({
                    'id': f'iacr_{paper_id}',
                    'iacr_id': paper_id,
                    'title': title,
                    'authors': authors,
                    'abstract': abstract,
                    'published': published_date.strftime('%Y-%m-%d'),
                    'source': 'IACR',
                    'pdf_link': pdf_link,
                    'url': entry.link,
                    'categories': ['Cryptography'],
                    'published_official': True  # IACR papers are preprints
                })

            print(f"Fetched {len(papers)} papers from IACR")

        except requests.RequestException as e:
            print(f"Error fetching from IACR: {e}")
        except Exception as e:
            print(f"Error parsing IACR feed: {e}")

        time.sleep(self.delay)
        return papers
