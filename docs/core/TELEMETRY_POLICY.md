# CONTRATO NORMATIVO — Telemetría MQTT: persistir por cambio y máximo N valores/período

**Prioridad P0, bloqueante para primer MVP.** Es la principal mejora funcional pedida respecto a la experiencia OpenRemote: ningún activo MQTT necesita pasar por Node-RED para reducir presión de almacenamiento.

## 1. Dos niveles de configuración
- `MqttAgent` tiene `history_policy_defaults`: política que se aplica a todos los atributos vinculados sin override.
- `AssetAttribute` define `storageDatapoint` (alias de UI/compatibilidad) / `history_enabled` (modelo interno) y `history_policy_override` opcional. Puede optar por `inherit`, reemplazar campos seleccionados o `disabled` y obliga a validar combinaciones.
- Al crear vínculo MQTT se muestra efectivo (`agent_default` + override), origen de cada parámetro y preview de muestras estimadas. En edición de atributo mostrar “almacenado: sí/no”, política efectiva y fuente. No confundir history policy con subscription QoS ni con alertas.
- En el admin permitir aplicar bulk policy a múltiples atributos con diff/preview y auditoría. Cambios efectivos son versionados con fecha UTC y usuario, sin reescribir silenciosamente históricos.

## 2. Modelo de configuración propuesta
```json
{
 "storageDatapoint": true,
 "history_policy": {
   "mode": "on_change",
   "compare": {"type": "numeric", "absolute_epsilon": 0.1,
               "relative_epsilon": null, "hysteresis": null},
   "max_samples": {"count": 60, "window": "1h", "strategy": "latest"},
   "heartbeat": {"max_silence": "24h", "quota_exempt": false},
   "timestamp_policy": "event_time_with_skew_validation",
   "quality_policy": "exclude_invalid_from_history"
 }
}
```
Las propiedades son diseño de OAP, no claims sobre APIs de terceros. Modes admitidos: `all`, `on_change`, `min_interval`, `fixed_n_per_window` (muestreo distribuido), `aggregate_window` (agregado con unidad/calidad). Composición: primero elegir candidatos por mode; luego aplicar `max_samples` como límite duro N para raw history en ventana T; política `latest` reemplaza candidato retenido en buffer de ventana si N agotado, pero NO reescribe filas ya confirmadas sin operación explícita. Requisito crítico: definir si N es máximo o objetivo por ventana; default es **máximo**, e `fixed_n_per_window` es modo separado. Claramente mostrar en UI.

## 3. Semántica de on_change
- Compara valor normalizado nuevo con última muestra **persistida aceptada** para history y opcionalmente con last observed para evitar oscillation; la referencia exacta elegida se documenta/expone en UI. En el baseline: comparar con **última persistida**; `last_observed` es estado actual y no baseline histórica.
- Tipos: bool/string/enum igualdad exacta; números `abs(new - baseline) > epsilon_abs` o combinación con tolerancia relativa bien definida; arrays/JSON usar comparador canónico con normalización y límite de tamaño; estados `null`/NaN/inf no tienen semántica de cambio ordinaria (manejar como quality_event).
- Primer valor válido persiste si storage habilitado y cuota lo permite. Cambios dentro epsilon no persisten. `false → true → false` debe persistir transiciones si cuotas lo permiten.
- `hysteresis` y debounce para sensor ruidoso deben ser explícitos, no deducidos. Escalado/calibración/unidad se aplica antes de comparar.
- Heartbeat es muestra opcional de continuidad tras máximo silencio, su impacto en N/T es claro y por defecto NO elude la cuota. Eventos de alarmas críticos no dependen de esta política.

## 4. Límite N muestras por ventana T
- Configuración `N` entero >=1, `T` duración ISO 8601 o sintaxis estricta (ej. `PT1H`) con UTC y límites operativos. `count=0` únicamente si significa disabled y validado; no tratar como unlimited. Política `hard_cap` se aplica por `(tenant, attribute, policy_version, ventana)` con límites atómicos al paralelizar.
- Default recomendado: ventanas fijas UTC con inicio `[floor(event_time / T)*T, ... )`; para políticas rolling/sliding se diseñará variante aparte; UI explica diferencia.
- Combinación con `on_change`: solo cambios significativos son candidatos y aun así no se guardan más de N. `mode=all` + cap N descarta muestras que excedan; `fixed_n_per_window` reserva ranuras temporales (no garantía de N si no hay eventos) y selecciona muestra más representativa por slot.
- `strategy=first` guarda primeras N; `latest` necesita buffer/upsert por ranura (especificar hasta dónde admite retrasos) y `uniform` distribuye los slots; no vender `latest` si solo se descartan tras N. Alternativa `aggregate_window` materializa min/max/avg/count/last con quality y timestamp, no se mezcla con raw sin contrato.
- Los intervalos con cambio de hora se calculan en UTC, las fechas UI se convierten a tz del proyecto; out-of-order y event time retroactivo deben respetar window finalization/watermark. Para evitar reescribir histórico de ventana sellada: late sample se rechaza con métrica o almacena en canal de corrections siguiendo política, nunca altera arbitrariamente cupos anteriores.
- Hay que evitar que dos workers inserten N+1 simultáneamente. Implementar atomicidad por DB constraint/locking o procesar serial por partición; tests concurrentes demuestran el límite.

## 5. Pipeline obligatorio (orden)
```
MQTT input -> authenticate/authorize device & tenant -> decode/validate schema
 -> normalize timestamp/quality/units -> deduplicate source event
 -> update last_observed + last_valid (transactional or consistent)
 -> rules/alarms/live events on all valid observed samples
 -> evaluate history_enabled & effective agent/attribute StoragePolicy
 -> persist accepted samples to PostgreSQL (batched/idempotent)
 -> update persisted baseline/window counters
 -> emit counters accepted/skipped_same/skipped_quota/skipped_invalid/late/replay
```
Si rule evaluation y persist son asíncronos, documentar ordering y replay; no perder alarmas por filtro storage. La política de almacenamiento N/T NO controla consumo de mensajes del broker ni reemplaza backpressure; ambos necesitan métricas.

## 6. Datos que deben almacenarse
- `AttributeCurrent`: tenant_id, project_id, asset_id, attribute_id, observed_at, value_type, typed_value, quality, source_event_id, ingest_time, version.
- `TelemetryPoint`: tenant_id, attribute_id, ts (event UTC), ingested_at, typed value/JSON, quality, policy_version, source_event_id/seq, UNIQUE lógico con dedupe.
- `StoragePolicy`: owner scope (agent/attribute), version, enabled, mode, compare, heartbeat, quota, window type, changed_by, created_at.
- `StoragePolicyState`: attribute_id, policy_version, last_persisted_value, ts, quota bucket/counter, watermark, durable state. Reiniciar worker NO resetea cuota ni last_persisted baseline.
- `IngestMetrics`: received, valid, invalid, duplicate, accepted, filtered_equal, filtered_quota, late, queue_backpressure, failures; cardinalidad controlada.

## 7. Replay, caída de conexión y consistencia
- MQTT QoS1 puede redeliver: dedupe por `source_event_id` o combinación estable de connection/topic/sequence/timestamp+hash (documentar limitación si originador no trae ID). No crear history duplicada tras restart.
- Si DB está temporalmente caída: buffer acotado o spooling cifrado cuando aplique, retry con backoff, indicadores de pérdida y DLQ; no convertir entrada silenciosamente en infinito uso RAM/disk.
- Si un atributo cambia de política: nueva versión; no recalcular históricos anteriores salvo operación administrativa explícita.
- Tiempo de dispositivo vs server: aceptar skew configurable, guardar ambos tiempos; muestras futuras o tardías se clasifican según política, sin alterar valores de ventana arbitrariamente.
- Orden de envío de comandos no se deduce de la serie histórica. Alarmas y estado deben tener su propia persistencia o outbox.

## 8. API REST y UI
- `GET /api/v1/mqtt/agents/{id}/storage-policy` / `PUT` con ETag/If-Match.
- `GET /api/v1/assets/{asset_id}/attributes/{attribute_id}/storage-policy/effective` muestra `source`, `history_enabled`, `mode`, `max_samples`, `window`, `estimated_rate`, `policy_version`.
- `PUT .../storage-policy` con permisos `telemetry.policy.write`; valida cuota, valores, tipos, lock env si aplica; 403/409/422 apropiados.
- `GET /api/v1/.../telemetry/stats` métricas de reducción y últimas muestras; accesible para auditoría.
- Editor de MQTT Agent: sección `Storage defaults`; editor atributo: `Store datapoints` y `Persist only when changed` + `Maximum samples per period`; preview efectivo y ejemplo de resultado.

## 9. Umbrales y aceptación (no solo conteo de archivos)
- Con 1000 eventos válidos del mismo valor `42` y `on_change`, current=42 y SOLO 1 fila histórica (sin heartbeat); metrics received=1000, accepted=1, filtered_equal=999.
- Con eventos `[1,1,2,2,3]`, comparar exacto, policy on_change, history `[1,2,3]`; el dashboard live recibió los 5.
- Con `max_samples.count=3`, ventana 1h UTC y 100 eventos diferentes, historia raw dentro ventana <=3, sin exceder por workers concurrentes o retry.
- Override de atributo `N=5` prevalece sobre agent default `N=2`; tras reinicio, ambos persisten; otro atributo sin override se queda en 2.
- Con un cambio importante después de cuota agotada: current refleja último cambio y reglas lo ven, mientras history raw sigue <=N; UI indica loss de history por cuota.
- Con `fixed_n_per_window=N`, muestras uniformemente seleccionadas por slots deterministas, y si se reciben menos de N NO se inventan datos.
- False positives: ruido dentro epsilon no persiste; NaN no corrompe last_valid, unit conversion precede compare.
- Restart de API/worker, DB persistente, replay MQTT QoS1: no duplicados ni cuota reseteada.
- Deberá comprobarse que el throughput bajo carga objetivo es suficiente sin dependencia Node-RED.

## 10. Anti-patrones bloqueantes
- Filtrar MQTT en Node-RED para cumplir on_change/N/T.
- Almacenar todos los eventos y limpiar después con cron; no previene saturación de escrituras.
- Hacer sampling antes de rules y alarms.
- Contador de cuota solo en memoria sin recuperación.
- Deshabilitar `storageDatapoint` como sustituto de “guardar solo cambios”.
- No distinguir frecuencia de publicación, número de valores guardados, cuota por ventana y política de retención.

Ver también `docs/quality/TELEMETRY_CASES.md`, `docs/contracts/TELEMETRY_SCHEMA.md`, `docs/plugins/mqtt/`.
