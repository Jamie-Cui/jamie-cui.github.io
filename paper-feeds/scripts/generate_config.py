#!/usr/bin/env python3
"""Generate frontend config from config.toml."""
import tomllib
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent

with open(APP_DIR / 'config.toml', 'rb') as f:
    config = tomllib.load(f)

papers_per_page = config.get('frontend', {}).get('papers_per_page', 10)

with open(APP_DIR / 'config.js', 'w') as f:
    f.write(f'const CONFIG = {{ papersPerPage: {papers_per_page} }};\n')
