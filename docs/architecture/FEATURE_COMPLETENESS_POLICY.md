# Cómo interpretar “reconstruir todas las funcionalidades”

La especificación debe guiar una implementación completa, pero ningún agente puede garantizar en un solo turno todos los features de un producto maduro. La paridad se verifica por feature inventory comparado contra repositorios `openremote/core` y `Grashjs/cmms` con commits fijos. La matriz separa `reference-feature`, `user enhancement`, `available-source`, `license`, `OAP owner`, `API/UI flows`, `tests` y `observed status`.

## No sustituir completitud por atajos
- Filtros de histórico en Node-RED ≠ soporte native MQTT Agent+Attribute on_change/N/T.
- Un CRUD sin roles/seguimiento/estado no equivale al CMMS Atlas.
- Un visor JSON no es constructor de dashboards.
- Un mapa SVG estático no cumple GIS+planos+georreferenciación.
- Exportar nombres en Turtle no constituye ontología validada Brick/Haystack.
- Un wrapper de APIs OpenRemote en paralelo no cumple el objetivo autónomo.
- Plugin toggle que no persiste reinicio no cumple administración extensible.
- Levantar Django sin DB extensions no cumple Timescale+PostGIS.

## Auditoría y cobertura
Mantener un test por capacidad y subcapacidad, señalar unsupported explícitamente, no liberar “100% parity” si quedan UNKNOWN/NOT IMPLEMENTED. Un hito puede ser MVP PASS con backlog abierto; ese status debe comunicar sin ambigüedad lo que funciona.
