"""
Progress display utilities for GitHub Actions.

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

import sys


class ProgressBar:
    """Simple progress bar that works in GitHub Actions."""

    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.last_percent = -1

    def update(self, n: int = 1):
        """Update progress by n items."""
        self.current += n
        percent = int((self.current / self.total) * 100) if self.total > 0 else 100

        # Only print when percentage changes to reduce output
        if percent != self.last_percent:
            bar_length = 40
            filled = int(bar_length * self.current / self.total) if self.total > 0 else bar_length
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\r{self.description}: [{bar}] {self.current}/{self.total} ({percent}%)",
                  end='', flush=True)
            self.last_percent = percent

            # Force newline at 100%
            if self.current >= self.total:
                print()

    def finish(self):
        """Mark progress as complete."""
        if self.current < self.total:
            self.current = self.total
            self.update(0)


def github_group(name: str):
    """
    Context manager for GitHub Actions collapsible groups.

    Usage:
        with github_group("Fetching papers"):
            # ... code ...
    """
    class GitHubGroup:
        def __init__(self, group_name):
            self.name = group_name

        def __enter__(self):
            print(f"::group::{self.name}")
            sys.stdout.flush()
            return self

        def __exit__(self, *args):
            print("::endgroup::")
            sys.stdout.flush()

    return GitHubGroup(name)


def github_notice(message: str):
    """Print a notice message in GitHub Actions."""
    print(f"::notice::{message}")
    sys.stdout.flush()


def github_warning(message: str):
    """Print a warning message in GitHub Actions."""
    print(f"::warning::{message}")
    sys.stdout.flush()


def github_error(message: str):
    """Print an error message in GitHub Actions."""
    print(f"::error::{message}")
    sys.stdout.flush()
