# Puertas de calidad G0–G9 — fail-closed

Una puerta PASS exige ejecución observada y evidencias, no existencia de archivos. Los gates son acumulativos: regresar a BLOCKED si falla una regresión. `scripts/quality_gate.sh` no debe retornar éxito con código incompleto.

| Gate | Lo mínimo que DEBE funcionar y probarse | Evidencia |
|---|---|---|
| G0 Spec | todos docs/core/plugins/quality, reglas Kilo, requisitos y rutas verificables, fuentes/licencias identificadas o pendientes | `check_spec_kit.py` + reporte |
| G1 Bootstrap | `.venv` creado primero; Docker fresh up; DB roles/extensiones/migrate automáticos; login/api/frontend healthy | logs `db-bootstrap`, `migrate`, tests Docker |
| G2 CORE | tenant/projects, activos+atributos, authz, REST, audit/outbox, pantalla CRUD | pytest+API+Playwright y casos deny |
| G3 Plugins/config | env defaults seed-once, enable/disable GUI, locks/dependencies, restart y upgrade preserving changes | E2E + DB assertions+restart |
| G4 MQTT history | subscribe directo, current/live, on_change Agent+Attribute, max N/T quota concurrent, no Node-RED | 1000-message fixture+TSDB SQL+metrics+restart |
| G5 CMMS | order/request/schedule/checklist/inventory con activo y permisos | unit+integration+E2E, timezones/races |
| G6 Semantic/GIS | IEC designations, Brick/Haystack mapping, RDF/SHACL; 2+ planos y geoposiciones, dashboards | triples + SHACL + PostGIS + MapLibre E2E |
| G7 Control/protocols | rules/alarms, CommandService, BMS/EMS, simuladores Modbus/BACnet/HTTP/Edge | fixture/HIL simulada, unauthorized fail |
| G8 Integraciones/IA | Node-RED import/export/deploy, ERP requisitions, MCP auth, assistant local opt-in | E2E contract integrations + no-secret |
| G9 Production | security, backups/restores, upgrades, performance, SBOM/licenses, paridad auditada | CI+staging reports y risk signoff |

## Comandos mínimos propuestos una vez que exista código
```bash
.venv/bin/python manage.py check --deploy
.venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python -m pytest -q
.venv/bin/python -m ruff check .
.venv/bin/python -m mypy backend  # configurar scope de mypy
npm --prefix frontend ci
npm --prefix frontend run lint
npm --prefix frontend run typecheck
npm --prefix frontend run test
npm --prefix frontend run test:e2e

docker compose config --quiet
docker compose build
docker compose up -d --wait  # verificar compatibilidad con versión Compose instalada
```
Estos comandos deben coincidir con scripts realmente creados; si no existen, reportar BLOCKED, no sustituirlos por `echo ok`.

## Bloqueos explícitos
- No saltar migraciones al fallar DB-extension; prohibido usar sqlite como sustituto final.
- No desactivar tests/security scanners para mostrar estado verde.
- No declarar paridad por tener endpoints vacíos, mocks permanentes, placeholder UI o pruebas smoke incompletas.
- No release con MQTT que dependa de Node-RED para persist only-on-change/N por período.
- No liberar contenedores como FOSS sin resolver licencias/atribuciones y dependencias.
