# Plugin `cmms` — especificación funcional y técnica

**Gate de aceptación:** G5. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
CMMS completo inspirado en Atlas: solicitudes, órdenes, preventivo/correctivo, calendario, medidores, downtime, checklists, recursos, mano de obra, historial, adjuntos y reportes.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `identity`
- `events`
- `notifications`
- `rules`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `WorkRequest(id,asset,requested_by,priority,status,description)`
- `WorkOrder(id,asset,status,priority,assigned_team,SLA,due_at)`
- `MaintenancePlan(id,asset,trigger=time|meter|condition,rrule,threshold,last_fired)`
- `WorkLog(order,technician,start/end,labor_cost,comments)`
- `ChecklistTemplate(version,items), ChecklistExecution(order,answers)`
- `Downtime(asset,start,end,reason,order_ref)`
- `PartReservation(order,part,qty,status)`
- `WorkOrderAttachment(storage_ref,content_type,hash)`

## Historias de usuario y workflows de extremo a extremo
1. Solicitud PENDING -> APPROVED/REJECTED (auditable); aprobación crea orden idempotente.
2. Orden NEW -> ASSIGNED -> IN_PROGRESS -> PAUSED -> COMPLETED -> CLOSED, con reopening autorizado y comentario obligatorio.
3. Plan de mantenimiento calendario o medidor/condición genera como máximo 1 orden por ciclo definido.
4. Registrar técnico, tiempos, repuestos usados, checklist, fotos/adjuntos y downtime sin pérdida de historia.
5. Alarma BMS puede crear propuesta de orden con dedupe por correlation_id; CMMS no actúa sobre equipo sin comando autorizado.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/cmms/requests` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/cmms/work-orders` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/cmms/work-orders/{id}:transition` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/cmms/plans` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/cmms/work-orders/{id}/logs` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/cmms/reports` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Kanban/tabla work orders, calendario preventivo, vista detalle con historia por activo
- Solicitud desde mapa/alarmas, checklist responsive para técnico

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_CMMS_DEFAULT_ENABLED`
- `CMMS_DEFAULT_TIMEZONE`
- `CMMS_ALLOW_REOPEN`
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
