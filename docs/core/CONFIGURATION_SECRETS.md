# CORE / Configuration Secrets

## Objetivo de producto y límites de propiedad
Configuración clara y auditada: variables de deployment, defaults iniciales, ajustes GUI y secretos fuera del repositorio.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `SettingDefinition(key, datatype, secret, mutable, restart_required, scopes)`.
- `SettingOverride(tenant/project, key, value, updated_by, revision)`.
- `SettingHistory(old_hash/new_hash, actor, timestamp)`.
- `SecretReference(name, provider, path, rotated_at)`.
- `DeploymentLock(key, forced_value, source)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET /api/v1/config/definitions`.
- `GET /api/v1/config/effective`.
- `PATCH /api/v1/config/overrides`.
- `POST /api/v1/config/overrides:reset-to-default`.

## Invariantes funcionales / reglas de negocio
- Infra/DB/secret files no son editables desde GUI.
- Si seed existe no reescribir al restart por `.env`. Locks explícitos prevalecen y se muestran como readonly.
- No guardar tokens/contraseñas en claro en `PluginSetting`, no GET secrets.
- Validar schema y transiciones con ETag, secret references y audit.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Cambiar plugin por GUI y reiniciar Compose sin perder preferencia.
- [ ] Secret nunca aparece en JSON, logs ni backup en claro sin cifrado.
- [ ] Dos admins simultáneos producen 409 por version.
- [ ] Defaults nuevos aplican a nueva instalación sin pisar personalizaciones.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
