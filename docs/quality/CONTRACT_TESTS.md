# Pruebas de contratos: REST, eventos, plugins, RDF, UI y MCP

## REST
OpenAPI generated de Django/DRF se parsea y tipa cliente TS; endpoint con rename requiere versionado. Responses schemas fijos, pagination/ETag/409 y validation errors uniformes. Auth matrix por usuario/servicio por tenant.

## Eventos
Producer schemas JSON compatibles con consumidores (CMMS, rules, ERP, semantic), outbox idempotente, DLQ y actor/scopes. Tests crash before/after publish y replay 3x. `telemetry.observed` se emite antes de history filter, `telemetry.persisted` sólo si aceptado.

## Plugin
Manifest semver compat, dependency cycles rejected, installed/enabled/health distinct, plugin disabled fallback, role/tenant activation. ETag de config y seed-once restart. UI plugin registry no sirve scripts externos.

## RDF/GIS
Triple URI stability, SHACL y graph tenant scoped, RDF projection lag; SceneLayer image coords local, GeoJSON geográfico con CRS correcto. React maps no recuperan capas de otro proyecto.

## MCP
Tool schema compatible con SDK pinned, tool read-only correcto, write requires proposal+approval+expiry; refusal no DB change; agent response no exfiltration. Tests client MCP real de integración cuando servidor implementado.

## Node-RED/ERP
Flow JSON export importable en Node-RED real test, con secrets omitidos; ERP callback signed, idempotency en requisiciones, retry y reconcile. Todo plugin opcional no afecta base sin estar instalado.
