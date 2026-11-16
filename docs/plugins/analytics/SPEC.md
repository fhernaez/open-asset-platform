# Plugin `analytics` — especificación funcional y técnica

**Gate de aceptación:** G9. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Reportes y dashboards configurables de telemetría, activos, alarmas, mantenimiento, energía y confiabilidad; consultas optimizadas y control de costes.

## Dependencias (contratos públicos; no imports privados)
- `telemetry`
- `cmms`
- `assets`
- `dashboards`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `SavedReport(id,owner,query_spec,format)`
- `MetricDefinition(name,formula,unit,aggregation,quality)`
- `ReportRun(id,params,status,artifact_ref)`
- `ExportJob(scope,format,limits)`

## Historias de usuario y workflows de extremo a extremo
1. Usuario define período, filtros y fuente autorizada; API optimiza agregaciones y ofrece CSV/JSON/PDF si plugin disponible.
2. Históricos muestreados reportan policy de sampling, calidad, porcentaje discarded.
3. CMMS cost/downtime MTTR/MTBF calculados con fixtures conocidos.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/analytics/reports` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/analytics/reports/{id}:run` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/analytics/metrics` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Constructor reportes y visualizador con filtros y exportación
- Indicador de integridad de dato para series muestreadas

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_ANALYTICS_DEFAULT_ENABLED`
- `REPORT_MAX_ROWS`
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
