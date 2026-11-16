# Plugin `dashboards` — especificación funcional y técnica

**Gate de aceptación:** G6. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Editor visual de dashboards y widgets BMS/EMS/CMMS/GIS con permisos por proyecto y componentes extensibles.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `telemetry`
- `spatial`
- `identity`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `Dashboard(project,scope,layout_version,layout)`
- `WidgetCatalog(type,plugin,config_schema)`
- `WidgetConfig(dashboard,metric_binding,display_units)`
- `DashboardShare(roles,public=false)`

## Historias de usuario y workflows de extremo a extremo
1. Crear dashboard, arrastrar widget de historia/estado/mapa/alarma y bindear a atributo.
2. Persistir layout versionado y revisar permisos de cada widget, incluso luego de disable addon.
3. Stream realtime y series history consumen API autenticada, no acceso directo a DB.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/dashboards` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/dashboards/{id}/widgets` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/widgets/catalog` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Drag-drop/resizable editor, chart history quality/aggregation
- Asset map / floorplan widget con layering, i18n

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_DASHBOARDS_DEFAULT_ENABLED`
- `DASHBOARDS_MAX_WIDGETS`
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
