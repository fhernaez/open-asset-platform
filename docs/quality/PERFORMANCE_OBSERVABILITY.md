# Rendimiento y observabilidad

## Instrumentación
Métricas OpenTelemetry si se configura: REST p50/p95/p99, tasks queue lag, DB wait, broker sessions, mqtt incoming per tenant, attr updates, historical writes, filtered_equal/quota/invalid/duplicate, rule execution, gateway offline, outbox retries, RDF projection lag, CMMS jobs, MCP tool failures, plugin health. Métricas con labels acotadas (no `asset_id` en series de alta cardinalidad por defecto).

## Carga reproducible
Preparar generador determinista (seed y payloads) en `.venv`, MQTT broker test, medir 10k mensajes/min y escalar por hardware. Caso 90% repetidos: history writes esperadas <=10% del modo all para la misma serie (más first/heartbeat, límites). Medir overflows, writer queue y memoria acotada; no afirmar throughput sin benchmark.

## BD
Indices por tenant/time/attribute, EXPLAIN ANALYZE de history y lookup de 1e6 points fixture, retención dentro de DB y muestras decimadas con visualización honesta (gap/quality). Si uso de date_trunc/compresion depende de licencia, revisarla y registrar alternativas FOSS.

## GIS/UI
1000 assets por vista y clustering/virtualization; no cargar SVG/tiles enormes sin límites; response stable y mapa offline. Dashboards paginan queries, cache de agregados con invalidez.

## Alerta de saturación
Storage free %, outbox lag, quota drop %, MQTT broker disconnect, rules worker starvation, DB bootstrap failures y backup age. Exportar dashboards de salud base sin plugins pagos.
