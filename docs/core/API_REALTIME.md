# CORE / Api Realtime

## Objetivo de producto y límites de propiedad
REST tipado, OpenAPI, realtime stream y sync incremental de datos de activos con auth y control de carga.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `APIVersion(v1)`.
- `Cursor(tenant, sequence, watermark)`.
- `RealtimeSubscription(principal, asset_refs, filters)`.
- `APIError(type,title,status,detail,request_id)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET /api/v1/openapi.json`.
- `GET /api/v1/assets?cursor=`.
- `GET /api/v1/telemetry/history`.
- `GET /api/v1/telemetry/current`.
- `WS /ws/v1/projects/{project_id}`.

## Invariantes funcionales / reglas de negocio
- Paginación límite por proyecto, rate limiting y filtros autorizados.
- Los eventos de WebSocket necesitan el mismo authz que REST, con refresh/revocation.
- Errores uniformes sin SQL trace ni secrets.
- ETag/If-Match en updates y schema/event versions en streams.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] OpenAPI válida y tipos TS cliente generables.
- [ ] Websocket no revela eventos de otro tenant.
- [ ] Paginación correcta en millón de points sin full scan.
- [ ] Malformed filter devuelve 400, no HTTP500.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
