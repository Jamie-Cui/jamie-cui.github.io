#!/usr/bin/env python3
"""Generate frontend config from config.toml."""
import tomllib
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = TOOL_DIR.parent.parent
PUBLIC_DIR = REPO_ROOT / "src" / "paper-feeds"

with open(TOOL_DIR / 'config.toml', 'rb') as f:
    config = tomllib.load(f)

papers_per_page = config.get('frontend', {}).get('papers_per_page', 10)

PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

with open(PUBLIC_DIR / 'config.js', 'w') as f:
    f.write(f'const CONFIG = {{ papersPerPage: {papers_per_page} }};\n')
