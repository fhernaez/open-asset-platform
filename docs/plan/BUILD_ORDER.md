# Plan de construcción secuencial para Kilo Code — NO crear todos los plugins de una vez

## Principios
Cada etapa produce un sistema usable y probado; dependencias deben estar PASS antes de activar implementación siguiente. Subagentes pueden preparar specs/tests en paralelo, nunca romper contratos. Todo Python LOCAL en `.venv`, primera acción `python3 -m venv .venv`. Todo Docker root no incluye OpenRemote/Atlas. Requisitos que aún no correspondan al MVP permanecen abiertos en matriz, no desaparecen.

**Estado de auditoría (2026-11-17):** repos de referencia auditados (`openremote/core` @ `6d46b473`, `Grashjs/cmms` @ `06abfe35` — `docs/research/`). Requisitos reestructurados en `OAP-MOD-NNN` (`docs/requirements/REQUIREMENTS.md`). El frontend se reconstruye de una vez (Ant Design + ECharts + mocks MSW) sobre contratos OpenAPI; cada gate conecta su backend real y activa sus pantallas (feature flags por gate; nada roto). La validación real de cada gate se ejecuta en el server del usuario con los scripts de `scripts/gates/`.

| Paso | Entregable verificable | Dependencias | Gate |
|---|---|---|---|
| S00 | Crear .venv, verificar tools y auditar license/source baselines; tests spec | Ninguna | G0 |
| S01 | Django/DRF + React app, Docker images, DB bootstrap roles/db/extensiones/migrate, login health | S00 | G1 |
| S02 | Tenants/Projects/AuthZ/Asset/Attributes/REST/OpenAPI/UI CRUD/outbox | S01 | G2 |
| S03 | Plugin registry, env seed-once, admin GUI toggle/locks/deps/restart | S02 | G3 |
| S04 | MQTT agent/broker, direct ingest, current+history policies on_change N/T agent+attribute | S03 | G4 |
| S05 | CMMS request/workorder/plans/checklists/time+Inventory | S04 | G5 |
| S06 | IEC 81346/Brick/Haystack RDF/SHACL + SpatialScenes two images/GIS + dashboards | S05 | G6 |
| S07 | Rules/alarms, command safety, BMS/EMS, simulators Modbus/BACnet/HTTP, edge | S06 | G7 |
| S08 | Node-RED JSON bidirectional, ERP connector, MCP, local AI opt-in | S07 | G8 |
| S09 | All remaining parity features, protocol gaps, native UX, load/security/backups/release audit | S08 | G9 |

## S00 — Antes de codificar
Leer documentación, crear `.venv`, comprobar scripts, fijar deps/versiones y commits de fuentes en `REFERENCE_LOCK`; revisar licencia; crear feature backlog/source graph como tarea explícita. Si no hay red, documentar auditoría pendiente sin frenar diseño propio de historias verificables.

## S01 — Bootstrap y vertical mínimo
Crear Dockerfiles y `compose.yaml` real con db, bootstrap, migrate, api, frontend. Prueba volumen nuevo Y preexistente sin DB. Página de salud (no claims paridad). Crear modelo Auth local seguro, migraciones versionadas y logs redacted. G1 bloquea S02 si falla.

## S02 — Asset transaccional
Un usuario puede login -> crear proyecto -> crear activo -> definir atributo tipado -> listar/paginar y editar -> ver audit. Otro tenant no puede. Outbox y UI E2E integran el circuito. No usar admin Django como frontend final.

## S03 — Plugins y configuración
Manifest, Django registry, settings seeded-once desde .env; UI admin list/toggle con lock y dependencias; restart y migración conserva preferencia. Real status installed/enabled/healthy; plugin in-process debe seguir importado aunque disabled.

## S04 — MQTT y política crítica
Direct MQTT Agent JSONPath, SSL/ACL, binding attrs, state and history. Implementar spec `TELEMETRY_POLICY.md` y todos los casos TEL-001–TEL-020 (algunos tests opcional del gate posterior si definición clara, pero TEL-001,002,005,006,008,009,010,020 bloquean). Sin Node-RED. Query current/history/UI, métrica de descartes.

## S05 — CMMS
WOs con transiciones verificadas, preventive triggers, meter/calendar/condition, checklist y asignaciones. Inventario técnico y coste laboral. ERP compras queda para S08, pero ya modelar external requisition link.

## S06 — Semántica/GIS/UI
IEC 81346 múltiples aspectos e historial, Brick/Haystack mapping, RDF/SHACL y tests. Escenas múltiples de imágenes en planos locales y geo MapLibre/PostGIS, overlays estado. Dashboards configurables. Demo hotel/rural.

## S07 — Control y operación
Rules engine declarativo + alarms, CommandService permisos/interlocks, BMS schedules, EMS metrics, adapters Modbus/BACnet/HTTP, edge caching. Empezar con simuladores; test coverage por protocolo antes de afirmar funcionalidad.

## S08 — Integraciones IA
Node-RED import JSON -> preview/commit y export tab versionado -> import real, trigger HTTP/MQTT. ERP requisition idempotente. MCP auth + tools/proposals, Ollama optional and RAG tenant-safe. Todo opt-in.

## S09 — Paridad y hardening
Auditoría fina repos por commit y grafos, cerrar todos gaps OpenRemote/Atlas o documentar explícitamente no conformidad; protocolos adicionales, analytics, móvil responsive, performance, security, FOSS, backups y restore.

## Checklist común final
Por cada Sxx: artefactos reales, migraciones, pruebas unit, integration, E2E, reporte logs+exit code, permisos, UI, docs, devops y evidence. Actualizar `docs/evidence/IMPLEMENTATION_STATUS.md` con tarea siguiente. Prohibido “S04 PASS” si sólo aparece `MqttAgent` en código sin broker+DB reales.
