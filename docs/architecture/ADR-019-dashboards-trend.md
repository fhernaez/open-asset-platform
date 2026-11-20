# ADR: Dashboards tipo ThingsBoard + objeto Tendencia

Estado: **Aceptada** (2026-11-19).

## Contexto

ThingsBoard (BUSL, solo patrón de referencia) organiza dashboards con grid configurable, catálogo de widgets por bundle, configuración por widget (series/ejes/umbrales/tema) y símbolos SCADA. OAP necesita un modelo equivalente para su arquitectura de datos.

## Decisión

1. **Grid drag/resize**: react-grid-layout; `Widget` conserva x/y/w/h y gana `config` validado por tipo (series, ejes y múltiples, umbrales, colores, tema, pestañas).
2. **Widget trend**: multi-serie (atributos del mismo o varios activos), multi-eje con rangos ajustables gráficamente, período seleccionable (última hora/24h/7d/30d o rango custom con zoom/brush); endpoint de historial multi-atributo con downsampling y flags de gap/quality.
3. **Bundles/templates**: `DashboardBundle` (export/import JSON de dashboard+widgets) y `DashboardTemplate` (plantillas reutilizables).
4. **Símbolos SCADA**: librería SVG básica + selector en el widget de mapa/plano (P2 dentro de esta iteración).

## Consecuencias

- Migraciones: config de widget sin cambio de tabla (JSON), `DashboardBundle`, `DashboardTemplate`.
- El botón "Ver como tendencia" desde Telemetría crea un widget trend con la serie actual.

## Alternativas consideradas

- Entidad Trend independiente: rechazada (widget con config multi-serie cubre el caso).
- Copiar widgets de ThingsBoard: rechazado (BUSL; solo patrones).
