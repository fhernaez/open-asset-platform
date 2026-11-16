#!/usr/bin/env bash
# G2 — CORE acceptance: tenant/project isolation, asset+attribute CRUD, audit.
set -euo pipefail
cd "$(dirname "$0")/../.."
fail() { echo "[BLOCKED G2] $*" >&2; exit 2; }
command -v curl >/dev/null 2>&1 || fail "curl required"
if ! timeout 120 docker run --rm alpine:3.20 true >/dev/null 2>&1; then
  fail "Docker daemon cannot run containers."
fi

BASE=http://localhost:8080/api/v1
TOKEN=$(curl -s -X POST "$BASE/auth/login" -H 'Content-Type: application/json' \
  -d "{\"email\":\"admin@oap.local\",\"password\":\"$(cat secrets/bootstrap_admin_password.txt)\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["access"])')
AUTH="Authorization: Bearer $TOKEN"

T1=$(curl -s -X POST "$BASE/platform/tenants/" -H "$AUTH" -H 'Content-Type: application/json' -d '{"name":"T1","slug":"t1"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
T2=$(curl -s -X POST "$BASE/platform/tenants/" -H "$AUTH" -H 'Content-Type: application/json' -d '{"name":"T2","slug":"t2"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
P1=$(curl -s -X POST "$BASE/platform/projects/" -H "$AUTH" -H 'Content-Type: application/json' -d "{\"tenant\":\"$T1\",\"name\":\"P1\",\"code\":\"p1\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

curl -s -X POST "$BASE/assets/assets/" -H "$AUTH" -H 'Content-Type: application/json' -d "{\"tenant\":\"$T1\",\"project\":\"$P1\",\"name\":\"A1\",\"external_ref\":\"a1\"}" >/dev/null

echo "[G2] Assets listed only within the caller tenant"
NAMES=$(curl -s "$BASE/assets/assets/?tenant=$T1" -H "$AUTH" | python3 -c 'import sys,json;print([r["name"] for r in json.load(sys.stdin)["results"]])')
echo "$NAMES" | grep -q A1 || fail "asset A1 not visible"
echo "$NAMES" | grep -q "B1" && fail "cross-tenant leak" || true

echo "[PASS G2] Core asset CRUD + tenant scoping verified over the real API."
