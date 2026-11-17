# CORE / Plugin Manager

## Objetivo de producto y límites de propiedad
Plugins del CORE o addons externos sin romper upgrades: declaración, compatibilidad, activación, estado operativo y UI de administrador.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `PluginDefinition(slug, version, core_api_range, capabilities, dependencies)`.
- `PluginInstallation(slug, artifact_version, kind, deployed_at, health)`.
- `PluginActivation(slug, scope, enabled, configured_by, revision)`.
- `PluginSetting(slug, scope, key, typed_value, origin, schema_version)`.
- `PluginLock(slug, reason, deployment_source)`.
- `PluginAuditEvent(old/new, actor, ts)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET /api/v1/plugins`.
- `GET /api/v1/plugins/{slug}`.
- `PUT /api/v1/plugins/{slug}/activation`.
- `GET/PUT /api/v1/plugins/{slug}/settings`.
- `GET /api/v1/plugins/{slug}/health`.

## Invariantes funcionales / reglas de negocio
- `.env` establece DEFAULT_ENABLED solo en bootstrap ONCE. Cambiar GUI persiste a restart.
- Installed != enabled != healthy; cambiar frontend toggle no cambia INSTALLED_APPS.
- Locks y dependencias prevalecen sobre GUI; Scope effective: global AND tenant AND project.
- Plugin disabled preserva datos históricos; no aceptar circular dependencies.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Definir env plugin CMMS=false, primer arranque lo deja false.
- [ ] Admin habilita CMMS y restart conserva true aunque env default sigue false.
- [ ] Lock hard deny plugin incluso admin; 409 si dependencia no disponible.
- [ ] Plugin ausente en imagen devuelve INSTALL_REQUIRED, no afirma activación.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
