"""
Keyword-based paper filter for Paper Feeds.

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

from typing import List, Dict
from pathlib import Path
import re


class KeywordFilter:
    """Filters papers based on keyword matching from a config file."""

    def __init__(self, config_file: str = None):
        """
        Initialize keyword filter.

        Args:
            config_file: Path to keyword configuration file
        """
        if config_file is None:
            config_file = str(Path(__file__).parent.parent / 'keywords.txt')

        self.config_file = config_file
        self.keyword_rules = self._load_keywords()

    def _load_keywords(self) -> List[List[str]]:
        """
        Load keywords from config file.

        Returns:
            List of keyword rules, where each rule is a list of keywords (AND logic)
        """
        rules = []

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Split by whitespace to get individual keywords
                    # Each keyword on the same line uses AND logic
                    keywords = [kw.lower() for kw in line.split()]
                    if keywords:
                        rules.append(keywords)

            print(f"Loaded {len(rules)} keyword rules from {self.config_file}")
        except FileNotFoundError:
            print(f"Warning: Keyword config file not found: {self.config_file}")
            print("Using default: accept all papers")
            # Return empty rules to accept all papers
            return []

        return rules

    def filter_papers(self, papers: List[Dict]) -> List[Dict]:
        """
        Filter papers based on keyword matching.

        Args:
            papers: List of paper dictionaries

        Returns:
            Filtered list of papers with added 'keywords' field
        """
        # If no rules, accept all papers
        if not self.keyword_rules:
            print(f"No keyword rules defined, accepting all {len(papers)} papers")
            for paper in papers:
                paper['keywords'] = []
                paper['keyword_score'] = 0
            return papers

        filtered = []

        for paper in papers:
            # Combine title and abstract for keyword matching
            text = f"{paper['title']} {paper['abstract']}".lower()

            # Check if any rule matches (OR logic between rules)
            matched_keywords = set()
            rule_matched = False

            for rule in self.keyword_rules:
                # Check if ALL keywords in this rule match (AND logic within rule)
                if self._rule_matches(text, rule):
                    rule_matched = True
                    matched_keywords.update(rule)

            if rule_matched:
                paper['keywords'] = list(matched_keywords)
                paper['keyword_score'] = len(matched_keywords)
                filtered.append(paper)

        print(f"Filtered {len(filtered)} papers out of {len(papers)} (matched keywords)")
        return filtered

    def _rule_matches(self, text: str, keywords: List[str]) -> bool:
        """
        Check if all keywords in a rule match the text (AND logic).

        Args:
            text: Text to search (lowercase)
            keywords: List of keywords that must all match

        Returns:
            True if all keywords match
        """
        for keyword in keywords:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if not re.search(pattern, text):
                return False

        return True
