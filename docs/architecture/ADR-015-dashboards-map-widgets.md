# ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes

Estado: **Aceptada** (2026-11-17).

## Contexto

Grafana aporta un catálogo de paneles verificado (timeseries, gauge, stat, barchart, table, state-timeline, status-history, **canvas** para fondos de imagen, **geomap** para capas geo) y ThingsBoard aporta el patrón de mapa por imagen con dispositivos posicionados (Image Map widget). OAP necesita dashboards con datos de telemetría reales y vistas georreferenciadas o sobre plano como funcionalidad priorizada.

## Decisión

1. **Modelo Dashboard/Widget/Grid** en backend: dashboards por tenant/proyecto con permisos; widgets referencian atributo(s) y visualización.
2. **Widgets del primer corte:** línea (ECharts), gauge, card (último valor), tabla, **mapa** con dos modos:
   - `plano`: una o varias imágenes locales (escenas), activos posicionados por coordenadas normalizadas, overlays de estado/alarma.
   - `geo`: capa MapLibre con activos por lat/lng, tiles offline opcionales.
3. **Escenas GIS y mapa global** (`OAP-GIS` v2):
   - `ProjectMapConfig` por proyecto: proveedor libre **MapLibre + OpenStreetMap** y `bounds` (norte/sur/este/oeste) definidas **navegando el mapa global y dibujando un rectángulo con el mouse**.
   - Ubicación de activos: **geográfica** (`latitude`/`longitude`, validada dentro de bounds cuando existe config) o **relativa** (escena + capa + x/y normalizados 0..1).
   - Placement por **pop-up**: el botón "Ubicar" junto al activo abre el mapa (proyectos geo) o la imagen del plano (proyectos relativos) y ubica con clic; los campos numéricos se sincronizan.
4. Los dashboards se conectan a telemetría real (current + history) vía los contratos de `OAP-TEL`; nunca mocks en producción. El **widget de mapa** elige modo: plano (escena+capa con placements) o geo (bounds del proyecto con assets por lat/lng), con selección de los activos a mostrar.

## Consecuencias

- La sección Mapas y el widget de mapa de Dashboards comparten el mismo motor de escenas (un solo bounded context GIS).
- Los widgets de mapa usan ECharts/Canvas propio y MapLibre; sin copia de código Grafana/ThingsBoard (AGPL/BUSL — ver `OAP-FOSS-001`).

## Alternativas consideradas

- Widgets solo de gráficas sin mapa: rechazado (prioridad del usuario: planos/geo).
- Motores de mapa externos (Google Maps como Atlas): rechazado por dependencia comercial; MapLibre + imágenes locales.
