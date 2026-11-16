# Fixtures de QA sintéticas

## Proyectos
`tenant-A`: hotel con 3 pisos y equipos Daikin VRV; `tenant-B`: red de alumbrado urbano, ambos con IDs UUID fijados en fixture (no nombres como IDs). Añadir site rural con medidor remoto, planta industrial con 2 tableros y bomba. Todo ficticio.

## Activos/semántica
Función de bomba / producto / ubicación, designación IEC con 3 aspectos, Brick equipment/point/room, tags Haystack, `oap:` predicate isFedBy; SHACL valid/invalid. Emplazamiento urbano lat/lon sintético, imágenes de prueba con dimensiones conocidas y georef control points.

## MQTT
Fixtures de `docs/quality/TELEMETRY_CASES.md` con 1000 repetidos, cambios y quotas. En mock evitar afirmar validación de QoS1/reconnect: publicar al broker de test real. Timestamp base UTC fijo para reproducibilidad.

## CMMS
WorkOrder por bomba, mantenimiento recurrente DST, 2 técnicos, 3 parts con stock, 2 ERP requisitions y webhook replay. Dos roles reader/admin para auth tests.

## Node-RED
`flows.json` con tab, 2 `mqtt in`, 1 `mqtt out`, broker config (sin auth) y 1 function no inferible. Export fixture con 1 tab y mapeo OAP IDs, y flow remoto modificado manualmente para conflicto.

## Seguridad
Payloads XSS labels, SVG malicious, webhook forged, SSFR target, JSONPath inválido, NaN/inf, publish wrong tenant, MCP invalid JWT y prompt injection para demostrar denegación.
