# `bacnet` — Operaciones paso a paso, API, UX y fallas

## Workflows normativos
### Flow 1: Descubrir dispositivo en red permitida (no escanear segmentos arbitrarios) y presentar assets/properties para aprobación.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.

### Flow 2: Leer propiedades con calidad e timestamps; COV con renewal y fallback poll controlado.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.

### Flow 3: Writes pasan CommandService y config de prioridad BACnet documentada y auditada.
- Preconditions: plugin installed and enabled, authentication and tenant/project scope verified, required dependency healthy.
- Positive path: validate inputs, execute through public DomainService, persist transactionally and emit versioned event.
- Negative path: invalid type, wrong tenant, duplicate request, unavailable dependency, concurrent edit -> reject/queue without partial side effect.
- Diagnostics: correlation ID, sanitised logs, retries and trace, observable status in UI.
- Test: add unit, integration with real backend and E2E if user-facing.


## Contrato HTTP a implementar y documentar
- `/api/v1/bacnet/devices:discover`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.
- `/api/v1/bacnet/devices/{id}/objects`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.
- `/api/v1/bacnet/devices/{id}/bindings`: define GET/list/create/update verb as permitted; DRF serializer JSON Schema; ETag/idempotency; tenant and project object permission; typed response and error codes; test 200/201/403/404/409/422.

## UI y formularios
- **UI-01:** Explorador de objetos BACnet con import preview. Expected: loading/empty/error/success, readonly lock, i18n ES/EN, keyboard accessibility.
- **UI-02:** Configurar poll/COV, prioridad escritura, estado comunicación. Expected: loading/empty/error/success, readonly lock, i18n ES/EN, keyboard accessibility.

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
