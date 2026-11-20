# Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE

Actualizado: 2026-11-17 (UTC). Código construido: backend Django/DRF (core, platforms, events, assets, telemetry, plugins, mqtt) + frontend React/TS + infra Docker/Compose. Sin dependencia operativa de OpenRemote/Atlas. **Arquitectura de datos: PostgreSQL + PostGIS, tablas regulares (ADR-013).**

## Fase 0 y Fase 1 — completadas (2026-11-17)

- **Auditoría de repos:** `openremote/core` @ `6d46b473`, `Grashjs/cmms` @ `06abfe35` y ampliación: ThingsBoard @ `80c1c615`, EdgeX (compose + device-mqtt/modbus/rest/virtual/snmp), Node-RED @ `f613ba10`, Grafana @ `f0b5ff91` — inventariados en `docs/research/` (`REFERENCE_LOCK.md`, `GRAPH_SOURCE_INDEX.md`, `RESEARCH_PATTERNS.md`).
- **Reespecificación:** `REQUIREMENTS.md` v2 (`OAP-MOD-NNN`, 20 módulos), `TRACEABILITY.md`, matrices PARITY auditadas, `SOURCE_TO_FEATURE.md`, `FEATURE_BACKLOG.md`.
- **Arquitectura v2 (2026-11-17):** menú canónico de 10 secciones en `MASTER_ARCHITECTURE.md` §9.1; **ADR-014** (Conectividad: Gateway como tipo de activo + bindings genéricas, reemplaza OAP-MQT→OAP-CON); **ADR-015** (dashboards con widget de mapa plano+geo, escenas GIS por imágenes). Orden de construcción reordenado en `BUILD_ORDER.md` (Activos→Conectividad/Telemetría→Plugins→Dashboards→Mapas→CMMS→Reglas→Integraciones→G9).
- **Contratos:** `drf-spectacular`; `docs/contracts/openapi.yaml`; `OPENAPI_CONTRACTS.md`.

## C1 — Tipologías y plantillas (2026-11-17)

- Backend: `AssetType.kind` (standard/gateway) + filtros por tenant/kind; plantillas de atributos (`schema.attributes`) aplicadas al crear activo con tipología; migración `assets/0004`.

## C2 — Catálogo, Conectividad y UX de Activos (2026-11-18)

- **Catálogo semilla** (`OAP-ASS-005/006`): `backend/assets/types_catalog/` con ~33 manifiestos completos (espacios/HVAC/energía/iluminación + tipos OpenRemote + 7 gateways con `connection_schema` por protocolo), validador, `seed_asset_types` idempotente por organización con `--refresh` (versionado + custom) y auto-siembra al crear organización.
- **Conectividad** (`OAP-CON-*`, ADR-014 v2): app `connectivity` (Gateway como activo de tipo gateway + GatewayBinding con `binding_type` attribute/device), worker multi-adapter con adapter MQTT real, **autodescubrimiento** de atributos con enable/disable (`auto_discovered`/`is_active`), test de conexión REAL (MQTT) y estado de conectividad derivado; alta de gateways desde Conectividad con formulario completo.
- **Dashboards + GIS** (ADR-015): `dashboards` (Dashboard/Widget con tipos line/gauge/card/table/map) y `spatial` (Scene/Layer con imágenes en `media/`, ScenePlacement con x/y normalizados); pantallas Dashboards (builder + widget de mapa plano) y Mapas (escenas, capas, placement por clic).
- **Admin + i18n**: AdminPage (settings de organización incl. locale + usuarios read-only); `Tenant.locale` default `es`; menú i18n es/en; versión visible en el footer.
- **Fixes**: `apiFetch` maneja 204 sin body (fin del error "Unexpected end of JSON input"); sanitización de `address` (caracteres de control); dropdown de proyectos con invalidación + error visible.
- Verificación: **55 pytest PASS**, ruff limpio, `npm lint/typecheck/test/build` PASS, OpenAPI regenerado, spec kit PASS.

## Pendiente (plan aprobado)

F5: validación real en el server del usuario (PostgreSQL/Mosquitto reales, E2E, `scripts/checklist`) → push + deploy. Reglas (G7) → CMMS (G5) → Integraciones/IA (G8) → G9.

## C4 — Semántica + jerarquía + 5 adapters + dashboards tipo ThingsBoard (2026-11-19)

- Backend: migración `assets/0006` (`is_location`, `rel_x/rel_y`, `geofence`, `image`, `designations`); designaciones 81346 versionadas con ocurrencia automática (`POST /assets/assets/{id}/designation/`); reglas de manifiesto validadas en create/update (422); proyección RDF (Brick/Haystack/OAP) + validación SHACL con `export_rdf`/`validate_semantics`; catálogo v3 con 11 tipos de ubicación (`is_location` + `designation_prefix` + `brick`).
- Backend: 5 adapters de protocolo (Modbus RTU/TCP, OPC-UA, BACnet, SNMP, CAN) con `run_forever`/`test` reales, registro único y worker multi-protocolo; pipeline compartido `ingest_device_payload` (autodescubrimiento agnóstico) para todos los transportes; `test_gateway_connection` delega al adapter.
- Backend: `POST /telemetry/trend` multi-atributo con downsampling (avg/LTTB) y flags de gap; `DashboardBundle` export/import, `DashboardTemplate` apply, catálogo de símbolos SCADA (`/dashboards/symbols/`), `ScenePlacement.symbol`; migración `dashboards/0002` + `spatial/0003`.
- Frontend: Sider colapsable manual; pestaña Jerarquía (árbol drag&drop con `PATCH parent` + maestro-detalle con designaciones); DashboardsPage con react-grid-layout (drag/resize persistido), widget `trend` multi-serie/multi-eje con período y gaps, bundles/templates UI, símbolos SCADA en widget mapa; i18n es/en.
- Evidencia: 82 pytest; ruff limpio; `makemigrations --check` sin cambios; OpenAPI regenerado (0 errores); npm lint/typecheck/test/build PASS; spec kit PASS.

## C3 — Idioma/timezone, usuarios, proyectos, MapConfig (2026-11-18)

- **Idioma/timezone**: resolución `User.locale/timezone` → `Tenant.locale/timezone` → `OAP_DEFAULT_LOCALE`/`OAP_DEFAULT_TIMEZONE` (env del servicio frontend servidas por `/config.js` con envsubst); formateo de timestamps con dayjs timezone.
- **Usuarios**: CRUD completo en Administración (crear con contraseña inicial + org/rol, editar idioma/timezone, activar/desactivar — nunca hard-delete).
- **Proyectos**: CRUD en Administración + comando `manage.py purge_project --code <código> [--yes]` (dry-run con conteos, borrado en orden de dependencias).
- **Mapas**: `ProjectMapConfig` con bounds dibujando un rectángulo sobre MapLibre+OSM; ubicación geográfica (lat/lng) o relativa (escena+capa+x/y); widget de mapa en dashboards.
- **Identificadores**: campo unificado "Código" con auto-sugerencia desde el nombre en todos los formularios; fix del selector de proyectos (opciones {value,label}).
- **Activos**: tipologías gateway ocultas del alta común (hint) + asociación opcional a un gateway (binding device automático).
- Verificación: **59 pytest PASS**, ruff limpio, `npm lint/typecheck/test/build` PASS, OpenAPI 0 errores, spec kit PASS, compose OK.

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
