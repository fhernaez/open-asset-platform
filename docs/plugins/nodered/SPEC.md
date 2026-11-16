# Plugin `nodered` — especificación funcional y técnica

**Gate de aceptación:** G8. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Interoperabilidad bidireccional con Node-RED: JSON export/import flow, reconstrucción de pestaña a partir de assets y triggers; Node-RED es OPCIONAL.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `mqtt`
- `semantics`
- `identity`
- `events`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `NodeRedInstance(url,secret_ref,env,project_scope)`
- `FlowMapping(flow_id,tab_id,asset_refs,point_refs,hash,version)`
- `FlowImportProposal(discovered_nodes,assumptions,conflicts)`
- `FlowDeployment(id,flow_id,revision,status)`
- `FlowTrigger(event_type,endpoint_or_topic,auth_config)`

## Historias de usuario y workflows de extremo a extremo
1. Import JSON/Admin API y parse nodes mqtt in/out/config, topics, JSONPath, transforms declarativas; detectar funciones JS no inferibles y marcar human-review.
2. Proponer assets y point bindings con diff, identificación canonical, duplicados y escenario no reemplazar derechos/proyecto; commit tras aprobación.
3. Exportar pestaña flow `tab` + nodes MQTT y opcionales transforms; placeholders secrets, metadatos OAP asset_id y hash, validar antes de POST /flow.
4. Actualizar flow existente con concurrency check/hash; divergence manual ofrece merge/review en lugar de overwrite.
5. Disparar proceso mediante webhook autenticado o MQTT evento; Admin API se reserva a gestión de flujos, no ejecución normal.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/integrations/nodered/import:preview` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/integrations/nodered/import:commit` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/integrations/nodered/export:preview` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/integrations/nodered/deploy` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/integrations/nodered/instances` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Asistente import/export con diff, conflicto y error semántico
- Lista flows desplegados/deriva, refresh/rollback lógico y permisos

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_NODERED_DEFAULT_ENABLED`
- `NODERED_BASE_URL`
- `NODERED_AUTH_SECRET_FILE`
Los defaults se importan ONCE a PostgreSQL; las preferencias administrables se editan en GUI y persisten al reinicio. Secret references no exponen credenciales. Los flags locked de deploy prevalecen.

## Riesgos específicos
- Una integración puede estar ausente, lenta o mal configurada: el CORE debe mantenerse operativo.
- Cambios de contrato requieren versionado, migraciones compatibles y regresión E2E; no modificar definiciones de activos ajenas.
- Para controles físicos aplicar `CommandService`, aprobación y tests en simulador; no ejecutar hardware real como parte del CI.
- Una capacidad listada no se considera implementada sin pruebas que ejerciten su efecto observable en base real/UI.

## Documentos vinculados
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/contracts/PLUGIN_CONTRACT.md`, `docs/contracts/EVENT_CATALOG.md`, `docs/quality/GATES.md`
- `{base}/ACCEPTANCE.md`
