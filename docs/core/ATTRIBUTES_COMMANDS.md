# CORE / Attributes Commands

## Objetivo de producto y límites de propiedad
Puntos de datos tipados, last_observed y comandos seguros; separar readonly telemetry de write intents.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `PointType(dtype, unit, min/max, quality_schema)`.
- `PointBinding(asset, attribute, protocol_link, read_path, write_path)`.
- `CommandRequest(idempotency_key, actor, target, payload, TTL, status)`.
- `CommandApproval(request, approver, expires)`.
- `CommandExecution(request, driver, ack, failure_reason)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET /api/v1/assets/{id}/points`.
- `POST /api/v1/commands:propose`.
- `POST /api/v1/commands/{id}:approve`.
- `POST /api/v1/commands/{id}:execute`.
- `GET /api/v1/commands/{id}`.

## Invariantes funcionales / reglas de negocio
- Validar rol/scope, data type, safe range y interlocks ANTES de enviar.
- No traducir cualquier mensaje de asistente a write de actuador.
- Estado actual no equivale a confirmación física de comando.
- Los comandos tienen expireAt, audit e idempotency key para retries.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/Timescale/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Un actuator fuera de rango devuelve 422 y no publica MQTT.
- [ ] Usuario read-only ni MCP sin aprobación pueden ejecutar.
- [ ] Comando expira o el device está offline: fallo auditable.
- [ ] Retry con misma idempotency key no provoca doble actuación.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
