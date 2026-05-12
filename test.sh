#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${1:-${PORT:-8080}}"

cd "$(dirname "$0")"

python3 build.py

echo "Serving _site at http://localhost:${PORT}/"
echo "Bound to ${HOST}. Press Ctrl-C to stop."

exec python3 -m http.server "${PORT}" --bind "${HOST}" --directory _site
