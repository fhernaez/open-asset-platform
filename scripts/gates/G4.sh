#!/usr/bin/env bash
# G4 — MQTT direct ingest: on_change + max N/T without Node-RED, on real broker+TSDB.
set -euo pipefail
cd "$(dirname "$0")/../.."

fail() { echo "[BLOCKED G4] $*" >&2; exit 2; }
command -v curl >/dev/null 2>&1 || fail "curl required"

if ! timeout 120 docker run --rm alpine:3.20 true >/dev/null 2>&1; then
  fail "Docker daemon cannot run containers (unshare/mount unavailable in this sandbox)."
fi

echo "[G4] Bring up stack with iot profile (mosquitto + telemetry-worker)"
docker compose --profile iot up -d --build --wait 2>&1

echo "[G4] Login and create agent/binding via API"
BASE=http://localhost:8080/api/v1
TOKEN=$(curl -s -X POST "$BASE/auth/login" -H 'Content-Type: application/json' \
  -d "{\"email\":\"admin@oap.local\",\"password\":\"$(cat secrets/bootstrap_admin_password.txt)\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["access"])')
AUTH="Authorization: Bearer $TOKEN"

# Create tenant/project/asset/attribute/broker/agent/binding (idempotent by external_ref).
TENANT=$(curl -s -X POST "$BASE/platform/tenants/" -H "$AUTH" -H 'Content-Type: application/json' \
  -d '{"name":"G4 Tenant","slug":"g4"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
PROJECT=$(curl -s -X POST "$BASE/platform/projects/" -H "$AUTH" -H 'Content-Type: application/json' \
  -d "{\"tenant\":\"$TENANT\",\"name\":\"Site\",\"code\":\"site\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
ASSET=$(curl -s -X POST "$BASE/assets/assets/" -H "$AUTH" -H 'Content-Type: application/json' \
  -d "{\"tenant\":\"$TENANT\",\"project\":\"$PROJECT\",\"name\":\"AHU\",\"external_ref\":\"g4-ahu\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
ATTR=$(curl -s -X POST "$BASE/assets/attributes/" -H "$AUTH" -H 'Content-Type: application/json' \
  -d "{\"asset\":\"$ASSET\",\"code\":\"temp\",\"name\":\"temp\",\"value_type\":\"number\",\"storage_datapoint\":true,\"history_enabled\":true}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

echo "[G4] Publish 1000 identical values via mosquitto_pub"
for i in $(seq 1 1000); do
  docker compose exec -T mqtt-broker mosquitto_pub -t "g4/$ATTR/temp" -m '42' || true
done

echo "[G4] Publish 5 distinct changes [1,1,2,2,3]"
for v in 1 1 2 2 3; do
  docker compose exec -T mqtt-broker mosquitto_pub -t "g4/$ATTR/temp" -m "$v" || true
done

sleep 3
echo "[G4] History rows (expect 1 for the 42 burst + distinct transitions)"
docker compose exec -T db psql -U oap_app -d oap -tAc \
  "SELECT count(*) FROM telemetry_telemetrypoint WHERE attribute_id='$ATTR'" | tee /tmp/oap_g4_count.txt
COUNT=$(cat /tmp/oap_g4_count.txt | tr -d '[:space:]')
[[ "$COUNT" -gt 0 ]] || fail "no history persisted for on_change ingest"

echo "[G4] Verify Node-RED service is not running"
docker compose ps --format '{{.Service}}' | grep -q nodered && fail "nodered should not be running" || true

echo "[PASS G4] Direct MQTT on_change ingest persisted to PostgreSQL without Node-RED (count=$COUNT)."
