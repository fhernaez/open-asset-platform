# `ems` — Operaciones paso a paso, API, UX y fallas

## Workflows normativos
### Flow 1: Vincular medidor y atributos energía/potencia con unidades y time zone.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.

### Flow 2: Calcular demanda punta/fuera punta y consumo por período con calidad/no gaps silenciosos.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.

### Flow 3: Simular PV/BESS peak shaving separado de control real, con reserva SoC y límites.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.

### Flow 4: Alertar demanda/consumo sobre umbral y disparar mantenimiento si data quality confirma.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.


## Contrato HTTP a implementar y documentar
- `/api/v1/ems/meters`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.
- `/api/v1/ems/tariffs`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.
- `/api/v1/ems/kpis`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.
- `/api/v1/ems/scenarios:simulate`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.

## UI y formularios
- **UI-01:** Dashboard consumo/potencia/savings e información de calidad. Expected: loading/empty/error/success, readonly lock, i18n ES/EN, keyboard accessibility.
- **UI-02:** Editor tarifas períodos, simulación sin actuación real. Expected: loading/empty/error/success, readonly lock, i18n ES/EN, keyboard accessibility.

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
Para cada flujo: prueba unitaria del dominio, integration contra PostgreSQL real y dependencias, happy/negative/tenant isolation, replay/concurrency cuando aplique, Playwright para UI y código documentado. QA independiente revisa antes de gate G7.
