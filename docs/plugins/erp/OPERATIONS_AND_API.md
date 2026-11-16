# `erp` — Operaciones paso a paso, API, UX y fallas

## Workflows normativos
### Flow 1: CMMS/Inventory solicita material -> outbox -> ERP adapter crea requisición con external reference.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.

### Flow 2: ERP aprueba/compra/recibe; webhook autenticado o poll actualiza estado replicado y enlaza a work order.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.

### Flow 3: Conflictos y retries usan idempotency/correlation ID; nunca factura/OC contable en OAP.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.


## Contrato HTTP a implementar y documentar
- `/api/v1/integrations/erp/connections`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.
- `/api/v1/integrations/erp/requisitions`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.
- `/api/v1/integrations/erp/webhooks/{connector_id}`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.

## UI y formularios
- **UI-01:** Configuración proveedor + mapping + test de conexión. Expected: loading/empty/error/success, readonly lock, i18n ES/EN, keyboard accessibility.
- **UI-02:** Estado de requisiciones externas por WO y reconciliación. Expected: loading/empty/error/success, readonly lock, i18n ES/EN, keyboard accessibility.

## Autorización y configuración
- Roles separados `view`, `operate`, `configure`, `admin`, más scopes por objeto. Deshabilitar global/tenant/project niega operaciones de escritura y oculta rutas UI sin perder registros.
- Endpoint de configuración informa valor efectivo y fuente (`code_default`, `env_seed`, `db_override`, `deployment_lock`), validación y revisión ETag.
- No devolver passwords, bearer tokens, client secrets, MQTT credentials, personal data de otros proyectos.

## Compatibilidad, error handling y health
- Runtime contenedor/plugin disabled no bloquea Django CORE. Implementar estado operacional y health con errores explicativos no ocultos.
- Si servicio externo no responde: circuit breaker/timeout/retries; operación idempotente por correlation ID o se deja pendiente.
- Publicar event schemas versionados y usar consumidores que toleren campos nuevos, sin depender de esquemas de otro addon.
- La pantalla muestra fallos reproducibles, no `success` optimista antes del resultado real del servidor.

## Definition of Done
Para cada flujo: prueba unitaria del dominio, integration contra PostgreSQL real y dependencias, happy/negative/tenant isolation, replay/concurrency cuando aplique, Playwright para UI y código documentado. QA independiente revisa antes de gate G8.
