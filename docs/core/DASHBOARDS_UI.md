# CORE / Dashboards Ui

## Objetivo de producto y límites de propiedad
Construir shell React extensible, gestor de activos, editor de dashboards, tendencias, mapas, alarmas, configuración y administración de plugins.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `Dashboard(id, scope, layout_json, revision)`.
- `WidgetDefinition(type, input_schema, capability)`.
- `WidgetInstance(dashboard, binding, options)`.
- `UIExtensionManifest(route, menu, permissions, version)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `GET/POST /api/v1/dashboards`.
- `PATCH /api/v1/dashboards/{id}`.
- `GET /api/v1/ui/extensions`.
- `GET /api/v1/widgets/catalog`.

## Invariantes funcionales / reglas de negocio
- Widgets no acceden directo DB ni cargan scripts remotos no auditados.
- UI muestra current + sampled history separadas; información de calidad/lag.
- MapLibre/mapas y planos integrados como widgets con permisos.
- Frontend estable al deshabilitar un plugin; routes ocultas y API devuelve 403/404.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/Timescale/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] E2E crear dashboard, asignar widget, guardar y reload.
- [ ] Deshabilitar addon oculta navegación sin borrar layout persistente.
- [ ] XSS en widget labels no ejecuta JS.
- [ ] Responsive ES/EN y accesibilidad básica teclado/ARIA.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
