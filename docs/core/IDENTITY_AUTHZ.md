# CORE / Identity Authz

## Objetivo de producto y límites de propiedad
Autenticación local bootstrap segura y OIDC opcional con Keycloak; autorización central usada por UI, API, WebSocket, MQTT y MCP.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `Principal(user/service/agent, tenant_id, status)`.
- `Role, Permission, RoleBinding(tenant/project/asset)`.
- `APIClient(id, scopes, expiry, secret reference)`.
- `PolicyDecision(actor, verb, object, project, context)`.
- `AuditEvent immutable logical record`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET /api/v1/me`.
- `GET/PUT /api/v1/roles`.
- `POST /api/v1/service-accounts`.
- `POST /api/v1/auth/rotate-credential`.

## Invariantes funcionales / reglas de negocio
- Autorización deny-by-default con objetos y herencia de scopes.
- Django superuser inicial creado sólo por bootstrap explícito, sin password hardcodeado.
- Tokens OIDC validar issuer/audience/exp/alg; service accounts scopes mínimos.
- MCP/agents impersonation prohibida; registrar actor original y delegación.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] 403 en UI/REST para rol insuficiente y en websocket subscription a asset ajeno.
- [ ] Revocación de token/role se propaga según TTL documentado.
- [ ] Rate-limit login/lockout y detección sesión inválida.
- [ ] Secretos nunca aparecen en responses, logs o export Node-RED.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
