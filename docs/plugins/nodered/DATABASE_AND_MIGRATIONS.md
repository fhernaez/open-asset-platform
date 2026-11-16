# `nodered` — Esquema de datos, constraints y migraciones

**No es SQL ejecutable todavía.** El agente debe materializar estos modelos como migraciones Django versionadas, con revisión de owner y contrato API antes de codificar. Django modelos no cambian cuando se deshabilita el plugin: deshabilitación funcional no borra tablas.

## Entidades y campos de negocio
1. `NodeRedInstance(url,secret_ref,env,project_scope)` — owner `nodered`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
2. `FlowMapping(flow_id,tab_id,asset_refs,point_refs,hash,version)` — owner `nodered`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
3. `FlowImportProposal(discovered_nodes,assumptions,conflicts)` — owner `nodered`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
4. `FlowDeployment(id,flow_id,revision,status)` — owner `nodered`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
5. `FlowTrigger(event_type,endpoint_or_topic,auth_config)` — owner `nodered`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.

## Convenciones de persistencia
- Cada tabla owner de plugin tiene UUID PK (o clave Timescale compuesta donde exija la extensión), `tenant_id`, `project_id` cuando los datos pertenezcan a un proyecto, `created_at`, `updated_at`, `revision`, `created_by` y `deleted_at` sólo para eliminación lógica cuando aplique.
- FK y restricciones de unicidad se diseñan con scope, no se aceptan IDs de otro tenant ni `ON DELETE CASCADE` que elimine historial técnico.
- Datos externos usan `(tenant, connector, external_id)` unique; replays y retries idempotentes; no doble alta de activos/órdenes/requisiciones.
- Campos sensibles referencian secretos gestionados fuera de DB; no conservar tokens en JSON arbitrarios.
- Registrar migraciones reversible/aditivas cuando viable, indexes para list/paginación y políticas de retención; operaciones destructivas requieren ADR+backup.

## Transacciones críticas
- Validar permisos de dominio primero, aplicar `select_for_update` o rev/version cuando hay carrera, persistir cambio y outbox en una misma transacción.
- Triggers externos nunca se ejecutan antes de commit. Webhooks se firman y se reintentan mediante worker.
- Cambio de plugin enabled no dispara `DROP TABLE`. Desinstalación necesita política de retención/export y aprobación.
- Datos `history` se preservan aun si el plugin queda disabled. Comprobar reconexión/replay cuando aplique.

## Índices y pruebas migratorias
- `tenant_id + project_id + created_at` para listas; `(external_system, external_id)` único en el scope correcto; indexes de estado/fecha para workflows.
- Aplicar migraciones sobre base NUEVA y RESTAURADA, con `makemigrations --check --dry-run` en `.venv` y base PostgreSQL/TimescaleDB real. Medir locks de migración en tablas con registros.
- Upgrade debe conservar estado, settings y referencia a activos; rollback de código sólo con schema compatible.
