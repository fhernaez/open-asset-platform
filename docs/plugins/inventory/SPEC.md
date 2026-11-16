# Plugin `inventory` — especificación funcional y técnica

**Gate de aceptación:** G5. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Inventario técnico CMMS con repuestos, almacenes, consumos, reservas, stock mínimo y costos; no contabilidad ni compras ERP nativas.

## Dependencias (contratos públicos; no imports privados)
- `cmms`
- `assets`
- `identity`
- `events`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `Part(id,sku,unit,catalog_ref,supplier_refs)`
- `Warehouse(id,location,tenant)`
- `StockBalance(warehouse,part,qty,version)`
- `StockMovement(part,warehouse,qty,signed,reason,order_id)`
- `StockReservation(part,work_order,qty,status)`
- `ReorderSuggestion(part,min_qty,external_requisition_ref)`

## Historias de usuario y workflows de extremo a extremo
1. Stock inicial por depósito, entrada y transferencia con movimiento auditable.
2. Orden reserva repuesto y al cerrar consume con transacción serializable o lock.
3. Stock bajo mínimo produce solicitud de abastecimiento para ERP connector, no orden de compra local.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/inventory/parts` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/inventory/warehouses` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/inventory/movements` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/inventory/reservations` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Catálogo y movimientos por depósito; stock/umbral en orden CMMS
- Vista solicitud a ERP y seguimiento referencia externa

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_INVENTORY_DEFAULT_ENABLED`
- `INVENTORY_NEGATIVE_STOCK_ALLOWED`
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
