# Contrato espacial — GIS/planos/escenas

## API models
`Location`, `SpatialScene(frame=local|geographic)`, `SceneLayer(type=image|svg|raster_tile|vector)`, `AssetPlacement(representation=physical|schematic|diagram)`, `SpatialTransform(matrix/control_points, error_rms, version)`, `GeoFeature(geom, SRID)`. Local XY in meters/units not EPSG:4326. Imágenes guardadas en object storage con checksum; evitar SVG ejecutable.

## Flujo frontend
Mapa regional → punto de predio → edificio → planta imagen A/B → sala → equipo. Escenas pueden compartir activo, distinto icono. Estado de alarmas/telemetría superpuesto por permisos, sin mezclar posición geográfica con topología. MapLibre proveedor default; mapas externos opt-in, offline selfhost supported.

## Endpoints
`POST/GET /api/v1/spatial/scenes`, `POST /scenes/{id}/layers`, `PUT /scenes/{id}/layers/{id}`, `POST /assets/{id}/placements`, `GET /scenes/{id}/features.geojson`, `POST /scenes/{id}/georef:preview`, `POST /scenes/{id}/georef:commit`.

## Edge cases
Cambio de resolución de imagen, CRS incorrecto, antimeridiano, lat/long invertidos, cotas verticales, planos con escalas distintas, límite tamaño raster, múltiples niveles, coordenadas nulas, geometrías inválidas, georreferenciación imprecisa. Reportar error y no fingir precisión. No descargar tiles OSM masivamente de servidor público.

## Validación
E2E cargar 2 JPG, cambiar orden/opacity, colocar dos activos, guardar, reload; geopunto aparece en mapa; sin permiso otro usuario no ve escena. Tests backend GeoDjango PostGIS geom transform valid y sanitized image.
