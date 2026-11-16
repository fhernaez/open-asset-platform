# Plugin `edge` — especificación funcional y técnica

**Gate de aceptación:** G7. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Gateways edge autohospedados: provisión, configuración por proyecto, buffering offline, sincronización y actualización segura.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `identity`
- `events`
- `telemetry`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `EdgeGateway(device_identity,tenant,project,cert_ref,version)`
- `EdgeDeployment(manifest,config_hash,desired/actual)`
- `EdgeSpool(sequence,event_count,checksum,encrypt)`
- `EdgeSyncCursor(gateway,last_acked_sequence)`

## Historias de usuario y workflows de extremo a extremo
1. Provisionamiento bootstrap por token expirable un solo uso y binding al tenant.
2. Gateway aplica conexiones/protocolos locales y almacena temporalmente al no tener red.
3. Reconectar, replay bounded, dedupe, reconciliar cambios autorizados sin doble control.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/edge/gateways` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/edge/gateways/{id}:enroll` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/edge/gateways/{id}/desired` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/edge/gateways/{id}/sync` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Lista gateways online/offline, últimos checks y versión
- Provisionar/rotar credenciales y estado de cola

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_EDGE_DEFAULT_ENABLED`
- `EDGE_SPOOL_MAX_MB`
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
