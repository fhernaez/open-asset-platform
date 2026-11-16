# Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE

Actualizado: 2026-11-13 (UTC). Código construido: backend Django/DRF (core, platforms, events, assets, telemetry, plugins, mqtt) + frontend React/TS + infra Docker/Compose. Sin dependencia operativa de OpenRemote/Atlas (no hay imágenes ni referencias runtime; solo el ADR-002 de auditoría).

## Resumen por gate

| Gate | Estado | Evidencia |
|---|---|---|
| G0 Spec | **PASS** | `.venv` creado primero; `scripts/check_spec_kit.py` → `SPEC VALIDATION: PASS` (206 md, 16 plugins) |
| G1 Bootstrap | **PASS (código) / BLOCKED (runtime Docker)** | compose.yaml válido; Dockerfiles; `ensure_db.py` idempotente; Docker daemon del sandbox no puede build/run (`unshare: operation not permitted`) |
| G2 CORE | **PASS (unit)** | 26 pytest (tenant isolation, asset CRUD, auth, audit) en SQLite (doble de test) |
| G3 Plugins | **PASS (unit)** | seed-once, core-no-disable, activation API (pytest) |
| G4 MQTT on_change N/T | **PASS (unit) / BLOCKED (broker+TSDB real)** | TEL-001,002,003,004,005,006,007,008,010,013,020 en pytest; broker/TSDB requieren Docker |
| G5-G9 | **BLOCKED** | no implementados (siguen hitos S05–S09) |

## Bloques de código entregados

- `backend/` — Django 6.0.10 + DRF + simplejwt + psycopg; apps `core`, `platforms`, `events`, `assets`, `telemetry`, `plugins`, `mqtt`; 10 migraciones versionadas.
- `backend/scripts/ensure_db.py` — bootstrap idempotente de role/DB/extensiones (postgis, timescaledb) con advisory lock.
- `backend/telemetry/storage.py` — pipeline de ingesta: current → rules → StoragePolicy → TSDB; `on_change` (epsilon abs/rel) y cuota `max_samples N/window T` con estado durable por atributo.
- `backend/mqtt/` — MqttAgent/BrokerConnection/MqttBinding + worker `mqtt_worker` (paho-mqtt) + ingesta directa vía JSONPath. **No usa Node-RED.**
- `compose.yaml` — db (timescaledb-ha:pg16), db-bootstrap, migrate, api, frontend, event-worker, mqtt-broker + telemetry-worker (perfil iot); secrets por archivo.
- `frontend/` — React 18 + TypeScript + Vite + nginx; login JWT y CRUD básico de activos.

## Comandos exactos para reproducir

```bash
cd /workspace/Open-Asset-Platform

# 1) venv (obligatorio, primero)
python3 -m venv .venv
.venv/bin/python -c 'import sys; assert sys.prefix != sys.base_prefix; print(sys.executable)'

# 2) dependencias backend + frontend
.venv/bin/python -m pip install -r backend/requirements.txt
.venv/bin/python -m pip install -r backend/requirements-dev.txt
npm --prefix frontend ci

# 3) checks + migraciones + unit tests (SQLite = doble de test)
(cd backend && ../.venv/bin/python manage.py check --deploy)
(cd backend && ../.venv/bin/python manage.py makemigrations --check --dry-run)
(cd backend && ../.venv/bin/python -m pytest -q)          # 26 passed
(cd backend && ../.venv/bin/python -m ruff check .)        # All checks passed
(cd frontend && npm run lint && npm run typecheck && npm run test)   # 1 passed

# 4) compose + secrets + runtime (requiere Docker con build/run habilitado)
bash scripts/gen_dev_secrets.sh
docker compose config --quiet
docker compose up -d --build --wait          # db -> db-bootstrap -> migrate -> api -> frontend
docker compose --profile iot up -d --wait    # añade mosquitto + telemetry-worker
```

## Bloqueo del sandbox (no es déficit de código)

`docker build`/`docker run` fallan en este entorno con `unshare: operation not permitted`
(vfs storage driver sin privilegios de montaje). Por ello la verificación de runtime
(G1 real, G4 real con broker+TSDB) queda **BLOCKED por ambiente**, no por código.
Cuando Docker esté disponible, ejecutar `bash scripts/quality_gate.sh G4` reproduce
la aceptación real (scripts `scripts/gates/G1.sh`..`G4.sh`).

## Requisitos cubiertos (traceability resumida)

SYS-001 (sin OpenRemote/Atlas), SYS-002 (compose+perfiles), SYS-003 (.venv), SYS-004/005 (bootstrap idempotente), CORE-001/002/003/007/008/009 (tenants/projects/assets/attributes/REST/outbox), CORE-010/011 (plugin registry+toggle), IOT-001..006 (MQTT agent, on_change, N/T, dedup, sin Node-RED).
