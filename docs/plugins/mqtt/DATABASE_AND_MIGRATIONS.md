# `mqtt` — Esquema de datos, constraints y migraciones

**No es SQL ejecutable todavía.** El agente debe materializar estos modelos como migraciones Django versionadas, con revisión de owner y contrato API antes de codificar. Django modelos no cambian cuando se deshabilita el plugin: deshabilitación funcional no borra tablas.

## Entidades y campos de negocio
1. `MqttAgent(id, tenant, broker_config_id, subscription_defs, storage_policy_defaults, connection_status)` — owner `mqtt`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
2. `BrokerConnection(host,port,tls,credentials_secret_ref,client_id,acl_scope)` — owner `mqtt`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
3. `MqttBinding(asset_id,attribute_id,subscribe_topic,publish_topic,json_path,qos,retain_policy)` — owner `mqtt`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
4. `MqttDiscoveryTemplate(topic_pattern,device_id_mapping,attribute_schema,approval_required)` — owner `mqtt`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.
5. `MqttSubscriptionHealth(agent,connectivity,received,published,backpressure)` — owner `mqtt`, must define UUID PK, project/tenant FKs when appropriate, indexes, validity and audit/version fields.

## Convenciones de persistencia
- Cada tabla owner de plugin tiene UUID PK (o clave compuesta), `tenant_id`, `project_id` cuando los datos pertenezcan a un proyecto, `created_at`, `updated_at`, `revision`, `created_by` y `deleted_at` sólo para eliminación lógica cuando aplique.
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
- Aplicar migraciones sobre base NUEVA y RESTAURADA, con `makemigrations --check --dry-run` en `.venv` y base PostgreSQL/PostGIS real. Medir locks de migración en tablas con registros.
- Upgrade debe conservar estado, settings y referencia a activos; rollback de código sólo con schema compatible.
