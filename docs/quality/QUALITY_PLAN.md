# Estrategia de verificación independiente

## Pirámide de pruebas
Unit: model validation, ACL logic, arithmetic/equality, timeslot, semantics, policy resolution. Integration: real PostgreSQL Timescale/PostGIS+Mosquitto+Node-RED test+MCP client, Django API, workers; E2E: Playwright React UI real y permisos. Contract: OpenAPI, JSON Schema events, plugin manifest. Security: SSRF, tenant isolation, secret leaks, authz commands. Performance: MQTT load, GIS large maps, DB query plans. Reliability: crash/retry/volume restart/backup restore.

## Política fail-closed
No pasar gate si no ejecutó test required. Coverage objetivo por rutas críticas >=90% branch (medido cuando exista código); coverage global sólo soporte, no excusa de no testear integraciones. Toda desviación pasa ADR y user review.

## Runbook CI
Crear `.venv` primero, install locked, run lint/type/test; Docker Compose config/build with ephemeral project; one-shot DB-bootstrap; API+web+MQTT smoke; test plugin restart; test DB existing volume missing app DB; security scan and SBOM. Publicar reports como artefactos de CI.

## Verificación humana
Los comandos a dispositivos físicos requieren laboratorio HIL/validación electricista/controlador, no confiar solamente en CI. UX y estándares IEC/ISO requieren revisión de experto; certificado no implícito.
