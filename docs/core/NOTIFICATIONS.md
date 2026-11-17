# CORE / Notifications

## Objetivo de producto y límites de propiedad
Sistema de notificación integrable email, webhooks, in-app y alerts push según canales instalados.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `NotificationTemplate(locale, channel, event_type)`.
- `NotificationPreference(user, severity, channel)`.
- `NotificationDelivery(message_id, status, retry)`.
- `EscalationPolicy(project, severity, schedule)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET /api/v1/notifications`.
- `POST /api/v1/notifications/{id}:read`.
- `GET/PATCH /api/v1/notification-preferences`.

## Invariantes funcionales / reglas de negocio
- Event IDs dedupe para evitar spam.
- No enviar correo real en tests, usar local sink.
- Opt-out por canales no críticos, escalamiento de alarmas críticas controlado.
- No secretos de SMTP en plantilla ni logs.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Alarma crítica entrega 1 notificación pese a replays.
- [ ] Preferencias por proyecto y usuario se respetan.
- [ ] Simular SMTP caído -> retries y failure visible.
- [ ] Template con HTML escape protege XSS.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
