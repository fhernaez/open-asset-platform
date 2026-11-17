#!/usr/bin/env bash
# G1 — Bootstrap acceptance: DB auto-provisioning (fresh + idempotent) and health.
set -euo pipefail
cd "$(dirname "$0")/../.."

fail() { echo "[BLOCKED G1] $*" >&2; exit 2; }

# Docker is the intended runtime; a daemon that cannot build/run images is a
# hard blocker for this gate (fail-closed, never a fake PASS).
if ! docker version >/dev/null 2>&1; then
  fail "Docker daemon unavailable; cannot run DB bootstrap acceptance."
fi
if ! timeout 120 docker run --rm alpine:3.20 true >/dev/null 2>&1; then
  fail "Docker daemon cannot run containers (unshare/mount unavailable in this sandbox)."
fi

command -v curl >/dev/null 2>&1 || fail "curl is required"
[[ -f compose.yaml ]] || fail "compose.yaml missing"

bash scripts/gen_dev_secrets.sh

echo "[G1] Fresh volume: docker compose up -d --build"
docker compose up -d --build --wait 2>&1

echo "[G1] Verify db-bootstrap completed and created role/db/extensions"
docker compose logs db-bootstrap | tee /tmp/oap_g1_bootstrap.log
grep -q "role_created=True db_created=True" /tmp/oap_g1_bootstrap.log || fail "db-bootstrap did not report creation"

echo "[G1] Verify migrate completed"
docker compose logs migrate | grep -q "bootstrap_config" || fail "migrate/bootstrap_config did not complete"

echo "[G1] API health"
code=$(curl -s -o /tmp/oap_g1_health.json -w "%{http_code}" http://localhost:8080/api/v1/health)
[[ "$code" == "200" ]] || fail "health endpoint returned $code"
cat /tmp/oap_g1_health.json

echo "[G1] Extensions present"
docker compose exec -T db psql -U postgres -d oap -tAc "SELECT extname FROM pg_extension WHERE extname IN ('postgis') ORDER BY 1" | tee /tmp/oap_g1_ext.txt
grep -q postgis /tmp/oap_g1_ext.txt || fail "postgis missing"

echo "[G1] Idempotency: re-run up + restart, no re-creation, same role/db"
docker compose up -d --wait 2>&1
docker compose restart db db-bootstrap 2>&1 || true
docker compose logs db-bootstrap | grep -q "role_created=False db_created=False" || fail "second run was not idempotent"

echo "[PASS G1] Bootstrap + idempotency verified on real PostgreSQL/PostGIS."
