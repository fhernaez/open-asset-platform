# Plugin `erp` — especificación funcional y técnica

**Gate de aceptación:** G8. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Conectores Odoo/ERPNext/ERP genérico para requisiciones técnicas, inventario externo opcional y seguimiento de compras sin recrear ERP ni OC propias.

## Dependencias (contratos públicos; no imports privados)
- `cmms`
- `inventory`
- `events`
- `identity`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `ErpConnection(provider,url,auth_secret_ref)`
- `PurchaseRequisitionLink(work_order,part,qty,external_ref,status)`
- `ErpSyncJob(idempotency_key,source_event,status,retry)`
- `ErpMapping(local_type,external_type,version)`

## Historias de usuario y workflows de extremo a extremo
1. CMMS/Inventory solicita material -> outbox -> ERP adapter crea requisición con external reference.
2. ERP aprueba/compra/recibe; webhook autenticado o poll actualiza estado replicado y enlaza a work order.
3. Conflictos y retries usan idempotency/correlation ID; nunca factura/OC contable en OAP.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/integrations/erp/connections` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/integrations/erp/requisitions` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/integrations/erp/webhooks/{connector_id}` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Configuración proveedor + mapping + test de conexión
- Estado de requisiciones externas por WO y reconciliación

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_ERP_DEFAULT_ENABLED`
- `ERP_PROVIDER`
- `ERP_BASE_URL`
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
