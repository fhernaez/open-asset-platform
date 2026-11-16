# Esquema de telemetría y políticas de almacenamiento

## Esquema de evento normalizado (`telemetry.observed.v1`)
```json
{
 "event_id": "uuid-or-stable-source-key",
 "tenant_id": "uuid",
 "project_id": "uuid",
 "asset_id": "uuid",
 "attribute_id": "uuid",
 "observed_at": "2026-11-13T17:00:00Z",
 "ingested_at": "2026-11-13T17:00:00.050Z",
 "value": 23.45,
 "value_type": "number",
 "unit": "Cel",
 "quality": "good",
 "source": {"agent_id": "uuid", "transport": "mqtt", "topic": "site/a/temp"},
 "sequence": 124
}
```
Todo timestamp en UTC con timezone; `value` se valida por PointDefinition, conversiones se realizan ANTES de reglas/history. Guardar `source_event_id`, evitar topic privado en logs públicos.

## Esquema StoragePolicy (`telemetry.storage-policy.v1`)
```json
{
 "storageDatapoint": true,
 "inherit_from_agent": true,
 "mode": "on_change",
 "compare": {"absolute_epsilon": 0, "relative_epsilon": null},
 "max_samples": {"count": 10, "window": "PT1H", "strategy": "first"},
 "heartbeat": {"max_silence": null, "quota_exempt": false},
 "late_event_policy": "reject",
 "invalid_quality": "skip_history"
}
```
`inherit_from_agent` y overrides son mutuamente interpretables: cuando false valores explícitos; cuando true campos no especificados heredan. El API effective debe mostrar fuentes y policy_version. `storageDatapoint=false` = no historial, current/rules continúan.

## Estados y métricas
Separate `AttributeCurrent`, `TelemetryHistory`, `PolicyVersion`, `PolicyState`, `StorageCounter` para received/accepted/filtered_same/filtered_quota/duplicate/invalid/late. Comparación de floats usa tolerancias documentadas. Quota por ventana fija UTC y atributo; concurrent safe. Ingesta no requiere Node-RED.

## Consultas
`GET /api/v1/assets/{id}/attributes/{attr_id}/current`, `GET /api/v1/.../history?from=...&to=...&resolution=...`, `GET .../policy/effective`, `GET .../history/stats`; responses incluyen policy metadata, unit, quality, gaps y cadence. Nunca inferir serie continua de muestras descartadas.

## Pruebas vinculantes
Referir `docs/core/TELEMETRY_POLICY.md` y `docs/quality/TELEMETRY_CASES.md`. Incertidumbre sobre interpretación de cuota debe resolverse preservando máximo N/T; no afirmar que muestreo uniforme garantiza N valores recibidos.
