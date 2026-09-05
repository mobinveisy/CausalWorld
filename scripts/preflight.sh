#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== CausalWorld preflight =="
python3 scripts/verify_release.py

echo
echo "== Web production build =="
cd web
npm install --no-audit --no-fund
npm run build

echo
echo "PRE-FLIGHT PASSED"
