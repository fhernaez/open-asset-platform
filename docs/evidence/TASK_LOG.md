# Bitácora de tareas verificables

Cada tarea debe dejar: fecha UTC, actor, historia, archivos, pruebas antes/después, resultados de comandos, failures, decisiones ADR, dependencias y siguiente paso. No copiar resultados de anteriores si cambiaron fuentes/versiones.

| Fecha | Historia | Agente | Comandos ejecutados | Evidencia | Resultado |
|---|---|---|---|---|---|
| 2026-11-13 | S00 sandbox+spec | lead | `python3 -m venv .venv`; `.venv/bin/python -c 'import sys; assert sys.prefix != sys.base_prefix'`; `.venv/bin/python scripts/check_spec_kit.py` | venv py3.14.2; docker 29.5.3; compose v2.40.3; node 24; SPEC VALIDATION: PASS | PASS |
| 2026-11-13 | S01 bootstrap backend | lead | `manage.py makemigrations`; `DB_ENGINE=sqlite manage.py migrate`; `manage.py check` | 10 migraciones; check 0 issues | PASS |
| 2026-11-13 | S02 core assets/authz | lead | `pytest tests/test_api.py` | login/me, tenant isolation, asset CRUD+audit | PASS |
| 2026-11-13 | S03 plugins | lead | `pytest tests/test_plugins.py` | sync idempotente, seed-once, core-no-disable, activation API | PASS |
| 2026-11-13 | S04 telemetry+Mqtt | lead | `pytest tests/test_telemetry_policy.py tests/test_mqtt_ingest.py` | TEL-001,002,003,004,005,006,007,008,010,013,020; MQTT direct ingest | PASS |
| 2026-11-13 | G1 runtime Docker | lead | `bash scripts/quality_gate.sh G1` | `docker run --rm alpine` → `unshare: operation not permitted` | BLOCKED (sandbox) |
| 2026-11-13 | infra compose+db bootstrap | lead | `docker compose config --quiet`; `pytest tests/test_db_bootstrap.py` | compose OK; 4 unit tests del orquestador bootstrap | PASS (unit) |
| 2026-11-16 | compose Komodo + CI GHCR | lead | `docker compose -f compose.komodo.yaml config --quiet` | secrets por env; db-bootstrap contra BD externa; workflow build-images.yml | PASS |
| 2026-11-17 | ADR-013 Postgres plano | lead | `DB_ENGINE=sqlite manage.py makemigrations telemetry`; `migrate`; `pytest -q`; `ruff check` | migración 0002 índice (attribute_id,-ts); 26 passed; ruff OK; ensure_hypertables eliminado | PASS |
| 2026-11-17 | F0 auditoría repos | lead | `git clone --depth 1 openremote/core`; `git clone --depth 1 Grashjs/cmms`; inventario paths (agent/manager/model/ui) | commits fijados `6d46b473` y `06abfe35`; 19 protocolos OpenRemote; 66 controllers + 50 modelos Atlas; licencias CDDL/GPL+TSL y AGPL/comercial; GRAPH_SOURCE_INDEX.md | PASS |
| 2026-11-17 | F0 reespecificación | lead | rewrites REQUIREMENTS/TRACEABILITY/PARITY_*/SOURCE_TO_FEATURE/FEATURE_BACKLOG/REFERENCE_LOCK + prompts/AGENTS/CONTEXT/.kilo | esquema OAP-MOD-NNN (20 módulos, ~90 IDs); estados SPECIFIED/PARTIAL/DONE | PASS |
| 2026-11-17 | F1 contratos OpenAPI | lead | `pip install drf-spectacular`; `manage.py spectacular --file docs/contracts/openapi.yaml --validate` | schema 4790 líneas validado; endpoints /api/v1/schema (+swagger); OPENAPI_CONTRACTS.md | PASS |
| 2026-11-17 | F3 G2 backend asset create | lead | fix serializers extra_kwargs + perform_create/update tenant pop + filtros query params | 27 pytest (nueva regresión admin sin membership); ruff OK | PASS |
| 2026-11-17 | F2 frontend rebuild (fundación) | lead | npm i antd/echarts/router/tanstack/msw/playwright; reescritura shell/ruteo/flags/login/assets | typecheck/lint/test/build PASS; MSW + ComingSoon por gate | PASS |

Decisiones ADR relevantes: apps empaquetadas fijas en `INSTALLED_APPS`; `platforms` (renombrado de `platform` para evitar colisión con stdlib); DB autoprovisionada por `db-bootstrap` one-shot con advisory lock; política de storage persistente en `StoragePolicyState` por atributo (quota/baseline durable ante restart); MQTT directo sin Node-RED. **ADR-013 (2026-11-17):** telemetría en tablas PostgreSQL regulares con índice B-tree `(attribute_id, ts DESC)` y dedupe `(attribute_id, dedupe_key)`; TimescaleDB diferido; imagen `postgis/postgis:16-3.4`; extensión única `postgis`.

Siguiente paso permitido: con Docker habilitado, ejecutar `bash scripts/quality_gate.sh G4` para cerrar G1–G4 en runtime real y continuar S05 (CMMS).
