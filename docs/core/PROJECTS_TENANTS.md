# CORE / Projects Tenants

## Objetivo de producto y límites de propiedad
Organizaciones y proyectos con roles, entornos y límites fuertes. Un activo y su historial no pueden transferirse a otro tenant con solo modificar parámetros HTTP.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `Tenant(id UUID, slug unique, status, locale, timezone)`.
- `Project(id, tenant_id, name, type, lifecycle, settings, version)`.
- `ProjectMembership(user_id, project_id, role, valid_from/to)`.
- `OrganizationLocation(project_id, parent_id, classification)`.
- `TenantQuota(tenant, assets, events, storage_bytes, users)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `POST/GET /api/v1/tenants (platform admin)`.
- `POST/GET/PATCH /api/v1/projects`.
- `GET/POST /api/v1/projects/{id}/members`.
- `POST /api/v1/projects/{id}/archive`.

## Invariantes funcionales / reglas de negocio
- Todos los querysets filtran tenant_id del principal; tenant no se deriva solo de un header controlado por cliente.
- Toda acción cruzada tenant requiere privilegio platform_admin y audit explícita.
- Projects pueden tener varios sites y zonas; jerarquías con ciclos prohibidos.
- Archivado no elimina historia ni rompe referencias CMMS/telemetría.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/Timescale/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Un usuario de tenant A recibe 404/403 para assets de B por URL e IDs adivinados.
- [ ] Renombrar proyecto no altera UUID ni referencias MQTT/GIS/CMMS.
- [ ] Cambios concurrentes usan optimistic locking (version/If-Match).
- [ ] Pruebas de enumeración y paginación no revelan otros tenants.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
