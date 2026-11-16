# CORE / Asset Registry

## Objetivo de producto y límites de propiedad
Un modelo técnico único de identidad, jerarquías y relaciones, separado de ubicación/función/producto IEC. Tipos de activos y atributos editables.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `Asset(UUID, tenant, project, name, type_id, lifecycle_state, external_refs, revision)`.
- `AssetType(schema_json, semantic_class, version, inherited_from)`.
- `AssetAttribute(id, asset_id, key, datatype, unit, writable, history_enabled, source)`.
- `Relation(subject_id, predicate_uri, object_id, valid_from/to)`.
- `ExternalReference(source, native_id, asset_id, unique(scope))`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `POST/GET/PATCH/DELETE /api/v1/assets`.
- `POST /api/v1/assets/import:preview`.
- `POST /api/v1/assets/import:commit`.
- `GET/POST /api/v1/assets/{id}/attributes`.
- `GET /api/v1/assets/{id}/relations`.

## Invariantes funcionales / reglas de negocio
- UUID inmutable; IEC reference y ubicación no son PK.
- Asset types versionados y JSON Schema validado, no schema libre sin guardas.
- Modificación/deletion debe considerar historial CMMS/telemetría; soft delete/retire.
- Búsqueda con filtros semánticos/GIS, paginación server-side.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/Timescale/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Crear activo con attr num+unit+agent, buscar, modificar, retirar y restaurar permisos.
- [ ] Duplicar external_ref crea conflicto claro y no segundo activo.
- [ ] Eliminación de activo con órdenes no borra audit/history.
- [ ] Consistencia transaccional en relaciones, prohibición de ciclos donde aplican.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
