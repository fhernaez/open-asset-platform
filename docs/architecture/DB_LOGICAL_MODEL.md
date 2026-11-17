# Modelo lógico SQL y owners

## Esquemas recomendados
`platform` (tenants, projects, roles, permission bindings, plugin registry/settings, config); `assets` (assets, types, attributes, designations, typed relationships); `telemetry` (current, histories, policy versions, counters, source event dedupe); `spatial` (locations, scenes, layers, placements, transforms); `events` (outbox, inbox, audit); `cmms` (work orders, requests, plans, logs, checks, parts, stock); `integrations` (refs, connections, jobs); `semantic` (assertion registry, RDF checkpoints). El esquema real puede ser un namespace de tablas Django app si usa search_path estándar; fijar decisión antes de migrar.

## Integridad
- `Asset.id UUID` PK; `tenant_id`, `project_id` y `revision` con índices.
- `AssetAttribute UNIQUE(asset_id,key)` si no versionado por key; `ExternalRef UNIQUE(tenant,source,external_id)`.
- `TelemetryHistory` tabla indexada por `(attribute_id, ts desc)` con `source_event_id` dedupe lógica; particionado nativo por tiempo es opción de escalado posterior, no una dependencia.
- `StoragePolicyState` requiere atomicidad per-attribute/window/policy_version para cuota N. Su serialización debe estar en DB o partición worker formal, no variable global de Python.
- `PluginActivation UNIQUE(plugin,scope,scope_id)`, `PluginSetting` con revisión ETag.
- `WorkOrder` tiene tenant/asset FK lógica por servicio/constraint; status transition audit y `WorkRequest` idempotency.
- `RDFProjectionCheckpoint` con tenant, seq, version; jamás autoridad de cambio.

## Migraciones
Schema migration versionada desde Django; PostGIS extensión vía `RunSQL` reversible cuando viable, con validación de extensión disponible en `db-bootstrap`. No usar `migrate --run-syncdb` como sustituto. Renovar índices con conciencia del costo de datos; sin `DROP` a menos que upgrade plan lo avale.

## Benchmarks
Explain Plan para 1e6 points y 100k assets, probar query hist policy, join filtrada tenant y index selectivity. Backup real y restore.
