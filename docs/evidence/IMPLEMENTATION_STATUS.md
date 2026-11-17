# Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE

Actualizado: 2026-11-17 (UTC). Código construido: backend Django/DRF (core, platforms, events, assets, telemetry, plugins, mqtt) + frontend React/TS + infra Docker/Compose. Sin dependencia operativa de OpenRemote/Atlas. **Arquitectura de datos: PostgreSQL + PostGIS, tablas regulares (ADR-013).**

## Fase 0 y Fase 1 — completadas (2026-11-17)

- **Auditoría de repos:** `openremote/core` @ `6d46b473`, `Grashjs/cmms` @ `06abfe35` y ampliación: ThingsBoard @ `80c1c615`, EdgeX (compose + device-mqtt/modbus/rest/virtual/snmp), Node-RED @ `f613ba10`, Grafana @ `f0b5ff91` — inventariados en `docs/research/` (`REFERENCE_LOCK.md`, `GRAPH_SOURCE_INDEX.md`, `RESEARCH_PATTERNS.md`).
- **Reespecificación:** `REQUIREMENTS.md` v2 (`OAP-MOD-NNN`, 20 módulos), `TRACEABILITY.md`, matrices PARITY auditadas, `SOURCE_TO_FEATURE.md`, `FEATURE_BACKLOG.md`.
- **Arquitectura v2 (2026-11-17):** menú canónico de 10 secciones en `MASTER_ARCHITECTURE.md` §9.1; **ADR-014** (Conectividad: Gateway como tipo de activo + bindings genéricas, reemplaza OAP-MQT→OAP-CON); **ADR-015** (dashboards con widget de mapa plano+geo, escenas GIS por imágenes). Orden de construcción reordenado en `BUILD_ORDER.md` (Activos→Conectividad/Telemetría→Plugins→Dashboards→Mapas→CMMS→Reglas→Integraciones→G9).
- **Contratos:** `drf-spectacular`; `docs/contracts/openapi.yaml`; `OPENAPI_CONTRACTS.md`.

## C1 — Tipologías y plantillas (2026-11-17)

- Backend: `AssetType.kind` (standard/gateway) + filtros por tenant/kind; plantillas de atributos (`schema.attributes`) aplicadas al crear activo con tipología; migración `assets/0004`.
- Frontend: Activos ahora con pestañas **Activos | Tipologías**; editor de tipologías con atributos de plantilla dinámicos; select de tipología en crear activo; 30 pytest PASS.

## Pendiente (plan aprobado)

C2 Conectividad (app `connectivity` reemplaza `mqtt`, gateway/bindings UI, adapters MQTT→Modbus) → Plugins UI → Dashboards (ADR-015) → Mapas/GIS → CMMS → Reglas → Integraciones/IA → G9. Validación real en el server del usuario.

## Resumen por gate

| Gate | Estado | Evidencia |
|---|---|---|
| G0 Spec | **PASS** | `.venv`; `check_spec_kit.py` → PASS; auditoría de fuentes ejecutada |
| G1 Bootstrap | **PASS (código) / BLOCKED (runtime Docker)** | compose válido; `ensure_db.py` idempotente; Docker del sandbox no corre contenedores |
| G2 CORE | **PARTIAL (unit)** | 26 pytest (tenant isolation, asset CRUD, auth, audit) en SQLite; bug conocido de creación de activos en UI (se corrige en el rebuild) |
| G3 Plugins | **PASS (unit)** | seed-once, core-no-disable, activation API (pytest) |
| G4 MQTT on_change N/T | **PASS (unit) / BLOCKED (runtime real)** | TEL-001,002,003,004,005,006,007,008,010,013,020 en pytest |
| G5-G9 | **BLOCKED** | diseñados (OAP-CMM/… en REQUIREMENTS v2), sin implementación |

## Bloques de código entregados

- `backend/` — Django 6.0.10 + DRF + simplejwt + psycopg; apps `core`, `platforms`, `events`, `assets`, `telemetry`, `plugins`, `mqtt`; 11 migraciones versionadas.
- `backend/scripts/ensure_db.py` — bootstrap idempotente de role/DB/extensión (`postgis`) con advisory lock.
- `backend/telemetry/storage.py` — pipeline de ingesta: current → rules → StoragePolicy → PostgreSQL; `on_change` (epsilon abs/rel) y cuota `max_samples N/window T` con estado durable por atributo.
- `backend/telemetry/models.py` — `TelemetryPoint` tabla regular: PK `id`, índice `(attribute_id, ts DESC)`, unique `(attribute_id, dedupe_key)`.
- `backend/mqtt/` — MqttAgent/BrokerConnection/MqttBinding + worker `mqtt_worker` (paho-mqtt) + ingesta directa vía JSONPath. **No usa Node-RED.**
- `compose.yaml` (local) — db `postgis/postgis:16-3.4`, db-bootstrap, migrate, api, frontend, event-worker, mqtt-broker + telemetry-worker (perfil iot); secrets por env.
- `compose.komodo.yaml` — variante para Komodo: BD externa por env, imágenes `ghcr.io`, red `iot-net`, puerto `${HTTP_PORT}`.
- `.github/workflows/build-images.yml` — publica imágenes backend/frontend en GHCR.
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
(cd frontend && npm run lint && npm run typecheck && npm run test)

# 4) compose + secrets + runtime (requiere Docker con build/run habilitado)
bash scripts/gen_dev_secrets.sh
docker compose config --quiet
docker compose up -d --build --wait          # db -> db-bootstrap -> migrate -> api -> frontend
docker compose --profile iot up -d --wait    # añade mosquitto + telemetry-worker

# 5) grafo de conocimiento (graphify, para consultas futuras con menos tokens)
graphify extract /workspace/Open-Asset-Platform --code-only
```

## Bloqueo del sandbox (no es déficit de código)

`docker build`/`docker run` fallan en este entorno con `unshare: operation not permitted`
(vfs storage driver sin privilegios de montaje). La verificación de runtime (G1 real, G4 real)
queda **BLOCKED por ambiente**. Con Docker disponible, `bash scripts/quality_gate.sh G4` reproduce
la aceptación real (`scripts/gates/G1.sh`..`G4.sh`).

## Requisitos cubiertos (traceability resumida)

SYS-001 (sin OpenRemote/Atlas), SYS-002 (compose+perfiles), SYS-003 (.venv), SYS-004/005 (bootstrap idempotente), CORE-001/002/003/007/008/009 (tenants/projects/assets/attributes/REST/outbox), CORE-010/011 (plugin registry+toggle), IOT-001..006 (MQTT agent, on_change, N/T, dedup, sin Node-RED). ADR-013: Postgres plano + PostGIS.
