#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "[BLOCKED] $*" >&2; exit 2; }
VENV="$PWD/.venv/bin"

[[ -f .venv/pyvenv.cfg ]] || fail "Missing .venv; first run: python3 -m venv .venv"
"$VENV/python" -c 'import sys; assert sys.prefix != sys.base_prefix' || fail "Python is not running in venv"
[[ -f backend/manage.py ]] || fail "Django source backend/manage.py does not exist"
[[ -f compose.yaml ]] || fail "compose.yaml missing"
[[ -f frontend/package.json ]] || fail "frontend/package.json missing"

echo '[GATE] Django system checks / migration checks'
(cd backend && "$VENV/python" manage.py check --deploy)
(cd backend && "$VENV/python" manage.py makemigrations --check --dry-run)
echo '[GATE] Unit tests'
(cd backend && "$VENV/python" -m pytest -q)
echo '[GATE] Static checks'
(cd backend && "$VENV/python" -m ruff check .)
echo '[GATE] Frontend checks'
(cd frontend && npm run lint)
(cd frontend && npm run typecheck)
(cd frontend && npm run test)
echo '[GATE] Compose configuration'
docker compose config --quiet

# Full runtime gates are invoked only for the implemented milestone target.
TARGET="${1:-G4}"
[[ "$TARGET" =~ ^G[1-9]$ ]] || fail "Invalid gate target: $TARGET (expected G1..G9)"
MAX="${TARGET#G}"
for ((i=1;i<=MAX;i++)); do
  gate="scripts/gates/G${i}.sh"
  [[ -x "$gate" ]] || fail "Missing mandatory runtime test runner: $gate; can't declare G${i} PASS"
  echo "[GATE] Executing G${i} real acceptance tests"
  bash "$gate" || fail "G${i} failed"
done
echo "[PASS] G1..${TARGET} scripts executed successfully. Check recorded evidence before signoff."
exit 0
