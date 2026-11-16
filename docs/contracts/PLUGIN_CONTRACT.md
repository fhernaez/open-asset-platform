# Contrato de extensibilidad OAP Plugin API v1

## 1. Objetivo y restricción Django
El core Django registra `INSTALLED_APPS` y migraciones al inicio; GUI habilita funcionalidad instalada, NO instala código ni modifica import path durante runtime. Plugins de alta independencia de dependencias son servicios externos versionados. API pública del núcleo es la única dependencia permisible a addons; prohibido importar `core.models._private` o manipular tablas ajenas.

## 2. Manifiesto (semántica a implementarse)
```yaml
id: oap.cmms
version: 1.0.0
core_contract: '>=1.0.0,<2.0.0'
kind: django_app
requires: [oap.asset_registry, oap.events]
provides: [maintenance.workorders, maintenance.preventive]
permissions: [cmms.view, cmms.manage, cmms.configure]
settings_schema_ref: schemas/cmms.settings.schema.json
ui_manifest_ref: frontend/cmms.extension.json
api_contract_ref: openapi/cmms.yaml
event_contract_ref: events/cmms-1.0.json
healthcheck: cmms.health
```
`requires` distinguir plugin instalable de core capability obligatoria. Validar inexistencia de ciclos en grafo dependencies y semver constraint. Manifest firmado/hash en release; no ejecutar hooks arbitrarios de paquetes no confiables con privilegio CORE.

## 3. APIs core para plugins
- `AssetService.get/list`, `AttributeService.read/write via CommandService`, `LocationService`, `SemanticService`, `ProjectService`.
- `EventPublisher.publish(domain_event, same_tx)`, `EventSubscription` declarativa, `JobScheduler` y `PluginConfigService` con scopes.
- `AuthzService.check(principal, permission, resource, project)`, `AuditService.record(...)`.
- `SpatialService.scene/placement`, `HistoryService.query/write` bajo permisos y retention.
- Todos los servicios aceptan un `RequestContext` con actor/tenant/project/trace, nunca solo `asset_id` sin contexto.

## 4. Instalación y habilitación
- `PluginDefinition`: en paquete/import registry, discovered on startup.
- `PluginInstallation`: versión realmente distribuida. No crear `ENABLE=true` como prueba de instalación.
- `PluginActivation`: global/tenant/project, default env seed-once, locks de deploy prevalecen, dependencies checked.
- `PluginSettings`: JSON Schema, diferenciación mutable/restart, secretos por referencia, ETag/audit.
- Cambio estado: drain jobs, desuscribir listeners, suspender nuevos triggers, mantener tablas/historia.

## 5. API REST propuesta
`GET /api/v1/plugins`, `GET /api/v1/plugins/{slug}`, `PATCH /api/v1/plugins/{slug}/activation` (If-Match requerido), `GET/PATCH /api/v1/plugins/{slug}/settings`, `GET /api/v1/plugins/{slug}/health`. Responses incluyen installed/enabled/effective/locked/health/restart_required/dependencies, por scope.

## 6. UI ExtensionManifest
`id`, `version`, `route`, `menuLabelI18n`, `permission`, `componentId` (registrado en bundle confiable), `widgets`, `settingsPanel`, `mapLayerTypes`, `helpLinks`. NO cargar scripts externos arbitrarios ni `eval` para un plugin importado. Plugin disabled oculta elementos pero no elimina saved dashboard configs; mostrar placeholder reversible.

## 7. Actualización y compatibilidad
Cambios de schema por etapas expand/contract, migrations forward-compatible, crash recovery y downgrade policy. Interfaces y eventos versionados; contrato compatible con core_api en CI. Un addon puede fallar sin tumbar API; plugins in-process no garantizan aislamiento de memoria, por eso deben ser confiables. Contenedores externos proporcionan aislamiento adicional.

## 8. Tests obligatorios
- Bootstrap env enabled=false; admin habilita true; restart y re-deploy conserva true.
- Locked disabled bloquea admin; dependency missing produce 409 sin DB inconsistente.
- Addon incompatible se marca INCOMPATIBLE y no registra sus operaciones.
- Desactivación de CMMS impide editar órdenes; CORE de activos sigue funcionando.
- Upgrade de core sobre datos existentes preserva plugin activation y migraciones.
