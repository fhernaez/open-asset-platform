# CORE / Spatial Scenes

## Objetivo de producto y límites de propiedad
Mapas basados en una o múltiples imágenes, coordenadas locales o GIS; navegación ciudad->predio->planta->sala con activo único.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `Location(id, parent, kind, semantic_ref)`.
- `SpatialScene(id, project, frame=local|geo, srid?, bounds)`.
- `SceneLayer(id, scene, source_type=image|vector|tile, z_index, opacity, source_ref)`.
- `AssetPlacement(id, asset, scene, geometry, representation_type, valid_from/to)`.
- `Georeferencing(control_points, transform, accuracy, version)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `POST/GET /api/v1/scenes`.
- `POST /api/v1/scenes/{id}/layers`.
- `POST /api/v1/assets/{id}/placements`.
- `GET /api/v1/scenes/{id}/features.geojson`.
- `POST /api/v1/scenes/{id}/georeference:preview`.

## Invariantes funcionales / reglas de negocio
- Las coordenadas en píxeles/metros locales no pueden etiquetarse EPSG:4326.
- Georreferenciación registra precisión, puntos control y matriz transformación.
- Imágenes múltiples y capas con orden/opacidad/control de acceso.
- MapLibre por default, Google Maps sólo opt-in y sujeto a TOS; permitir mapas offline.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Dos planos sobre la misma ubicación sin duplicar activo.
- [ ] Cambiar resolución imagen conserva ubicación local mediante transformación.
- [ ] GeoJSON SRID 4326 e imagen local se renderizan separados.
- [ ] ACL impide ver ubicaciones de proyecto ajeno; carga segura SVG.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
