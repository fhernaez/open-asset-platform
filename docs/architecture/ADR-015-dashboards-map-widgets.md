# ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes

Estado: **Aceptada** (2026-11-17).

## Contexto

Grafana aporta un catálogo de paneles verificado (timeseries, gauge, stat, barchart, table, state-timeline, status-history, **canvas** para fondos de imagen, **geomap** para capas geo) y ThingsBoard aporta el patrón de mapa por imagen con dispositivos posicionados (Image Map widget). OAP necesita dashboards con datos de telemetría reales y vistas georreferenciadas o sobre plano como funcionalidad priorizada.

## Decisión

1. **Modelo Dashboard/Widget/Grid** en backend: dashboards por tenant/proyecto con permisos; widgets referencian atributo(s) y visualización.
2. **Widgets del primer corte:** línea (ECharts), gauge, card (último valor), tabla, **mapa** con dos modos:
   - `plano`: una o varias imágenes locales (escenas), activos posicionados por coordenadas normalizadas, overlays de estado/alarma.
   - `geo`: capa MapLibre con activos por lat/lng, tiles offline opcionales.
3. **Escenas GIS** (`OAP-GIS`): escena = conjunto de imágenes (capas), CRS simple (normalizado 0..1 en el primer corte), placement de activos por clic sobre el plano o por lat/lng; export/import de la configuración de escena.
4. Los dashboards se conectan a telemetría real (current + history) vía los contratos de `OAP-TEL`; nunca mocks en producción.

## Consecuencias

- La sección Mapas y el widget de mapa de Dashboards comparten el mismo motor de escenas (un solo bounded context GIS).
- Los widgets de mapa usan ECharts/Canvas propio y MapLibre; sin copia de código Grafana/ThingsBoard (AGPL/BUSL — ver `OAP-FOSS-001`).

## Alternativas consideradas

- Widgets solo de gráficas sin mapa: rechazado (prioridad del usuario: planos/geo).
- Motores de mapa externos (Google Maps como Atlas): rechazado por dependencia comercial; MapLibre + imágenes locales.
