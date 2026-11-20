# ADR: Jerarquía de activos, activos de ubicación y navegación arbórea

Estado: **Aceptada** (2026-11-19).

## Contexto

OpenRemote estructura los activos en jerarquías navegables (group/city/building/room/thing…, reordenables por drag&drop). Las normativas 81346/ubicación requieren que cada activo tenga una posición inequívoca (función/producto/ubicación/tipo) y que los activos de ubicación definan el espacio donde viven sus hijos.

## Decisión

1. **Jerarquía**: `Asset.parent` (ya existe) es la fuente del árbol; el re-parenting por drag&drop valida tipos (un asset de ubicación no puede colgar de un equipo) y ámbito (mismo tenant).
2. **Activos de ubicación**: `AssetType.is_location` marca los tipos de sitio (city/building/floor/room/apartment/area/field/zone/parking, genéricos group/thing no son location). Un asset location tiene `geofence` (polígono GeoJSON dibujado sobre MapLibre+OSM) **o** `image` propia (upload a media/).
3. **Ubicación de hijos**: heredan del ancestro-location más cercano — imagen → `rel_x`/`rel_y` normalizados sobre la imagen del ancestro; geofence → `latitude`/`longitude` validada dentro del polígono. Las `Scene`s quedan como planos compartidos opcionales.
4. **UI**: Sider colapsable (botón toggle); Activos/Mapas/Telemetría comparten el mismo árbol (menú izquierdo) con filtros por tipología/ubicación/nombre; panel maestro-detalle a la derecha.

## Consecuencias

- Migraciones: `Asset.rel_x/rel_y`, `Asset.geofence`, `Asset.image`, `Asset.designations`; `AssetType.is_location`.
- El widget de mapa (dashboards) y la pantalla Mapas renderizan location assets (imagen o polígono) con sus hijos posicionados.

## Alternativas consideradas

- Solo Scenes como superficies: rechazado (el usuario definió que el location asset es la superficie).
- Geo únicamente: rechazado (se requieren planos/imágenes locales).
