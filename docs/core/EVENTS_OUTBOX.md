# CORE / Events Outbox

## Objetivo de producto y límites de propiedad
Entrega fiable y desacoplada de eventos y notificaciones, con reintento y dedupe.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `DomainEvent(id, tenant, aggregate_id, aggregate_version, schema_version, occurred_at)`.
- `OutboxEntry(event, published_at, attempt, next_retry)`.
- `InboxDedup(consumer_id,event_id,processed_at)`.
- `DeadLetter(event, reason, failed_at)`.
- `WebhookSubscription(owner,url,secret_ref,event_types)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET /api/v1/events/audit`.
- `POST /api/v1/integrations/webhooks`.
- `GET /api/v1/integrations/webhooks/{id}/deliveries`.

## Invariantes funcionales / reglas de negocio
- Outbox insertada EN MISMA transacción que el cambio de negocio.
- At-least-once con consumer idempotente, no afirmar exactly once.
- Retries exponenciales con jitter y DLQ visible.
- Webhook HTTPS con allowlist/SSRF guard, firma HMAC y replay window.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/Timescale/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Crash después de DB commit y antes publish: event se reenvía una sola vez al consumer.
- [ ] Entrega duplicada no duplica orden CMMS.
- [ ] Webhook a loopback o IP privada bloqueado por defecto.
- [ ] Schema v1/v2 transform compatible o rechazo controlado.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
