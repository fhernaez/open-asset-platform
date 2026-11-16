#!/usr/bin/env bash
# G3 — Plugin activation: seed-once, GUI toggle, restart persistence.
set -euo pipefail
cd "$(dirname "$0")/../.."
fail() { echo "[BLOCKED G3] $*" >&2; exit 2; }
command -v curl >/dev/null 2>&1 || fail "curl required"
if ! timeout 120 docker run --rm alpine:3.20 true >/dev/null 2>&1; then
  fail "Docker daemon cannot run containers."
fi

BASE=http://localhost:8080/api/v1
TOKEN=$(curl -s -X POST "$BASE/auth/login" -H 'Content-Type: application/json' \
  -d "{\"email\":\"admin@oap.local\",\"password\":\"$(cat secrets/bootstrap_admin_password.txt)\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["access"])')
AUTH="Authorization: Bearer $TOKEN"

echo "[G3] mqtt plugin is enabled by default (env seed)"
curl -s "$BASE/plugins/" -H "$AUTH" | python3 -c 'import sys,json; d={p["slug"]:p for p in json.load(sys.stdin)}; assert d["oap.mqtt"]["enabled"] is True, "mqtt not enabled"'

echo "[G3] Disable mqtt via GUI"
curl -s -X PATCH "$BASE/plugins/oap.mqtt/activation/" -H "$AUTH" -H 'Content-Type: application/json' -d '{"enabled":false}' | python3 -c 'import sys,json; assert json.load(sys.stdin)["enabled"] is False'

echo "[G3] Restart api; activation must persist disabled"
docker compose restart api >/dev/null 2>&1
sleep 5
curl -s "$BASE/plugins/" -H "$AUTH" | python3 -c 'import sys,json; d={p["slug"]:p for p in json.load(sys.stdin)}; assert d["oap.mqtt"]["enabled"] is False, "activation reset after restart"'

echo "[PASS G3] Plugin seed-once + toggle + restart persistence verified."
