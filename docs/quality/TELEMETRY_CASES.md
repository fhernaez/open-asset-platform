# Casos deterministas para almacenar solo cambios y máximo N/T

**Setup test:** stack Compose aislado con PostgreSQL/PostGIS, broker MQTT, telemetry-worker, Django API, current store, Redis/queue sólo si elegida, fixtures JSON. Crear Agent A en tenant T y atributos `temp`, `state`, `pressure`, cada uno con id real, policy persistida. Confirmar `storageDatapoint=true` y policies efectivas vía API ANTES de publicar. Conteos: SQL real history + API current + counters de worker + reglas live; no usar mocks como evidencia de integración.

| Test ID | Setup | Input | Resultado EXACTO esperado |
|---|---|---|---|
| TEL-001 | agent on_change epsilon=0 cap off | 1000 veces numeric 42 | history=1, current=42, 1000 observados, filtered_equal=999 |
| TEL-002 | on_change exact | 1,1,2,2,3,3 | history=[1,2,3], current=3 |
| TEL-003 | bool equality | false,false,true,false | history=[false,true,false] |
| TEL-004 | epsilon abs=0.1 | 20.0,20.05,20.09,20.2 | history=[20.0,20.2], current=20.2 |
| TEL-005 | agent maxN=2 PT1H, attr override maxN=5 | 100 changes on each | agent inherited attr <=2; overridden <=5, current final both |
| TEL-006 | maxN=3 PT1H | 1000 random changed numbers, 4 workers | history<=3 in same fixed window UTC, no race |
| TEL-007 | windows hourly | 4 events 00:59:59 and 4 01:00:01 UTC, N=2 | <=2 each of two windows |
| TEL-008 | history_enabled=false | 10 distinct values | history=0, current last, rules got 10 |
| TEL-009 | quotas exhausted | event triggers alarm after quota | alarm raised, history<=N, current fresh |
| TEL-010 | restart and replay | publish QoS1 IDs repeated, restart worker mid-hour | no duplication and no quota reset |
| TEL-011 | event_time skew | future, late beyond watermark | per policy invalid/late counted, no DB corruption |
| TEL-012 | JSON stable canonical compare | dict key-order swapped | no phantom changes |
| TEL-013 | invalid numeric | null, NaN, Inf, wrong units | quality flags, no invalid history, no crash |
| TEL-014 | fixed_n_per_window | 60 events evenly spread, N=6 | <=6 chosen slots, representative timestamps |
| TEL-015 | 3 events with N=6 | 3 valid events only | <=3, never invent filler points |
| TEL-016 | agent policy edit while streaming | N=2→N=5 | policy versions durable, deterministic cutover |
| TEL-017 | DB unavailable | 200 messages with limited spool | bounded memory, metrics and retry/explicit loss |
| TEL-018 | two tenants same topic textual | ACL scoped to T1/T2 | no cross-tenant leak or history |
| TEL-019 | browser plot history with skipped | 1000 repeated | UI indicates only 1 saved and why, no fake continuous series |
| TEL-020 | Node-RED not installed | normal MQTT ingest | TEL-001–019 functionality works without Node-RED |

## Fixture generator
Crear `tests/fixtures/telemetry_cases.json` y script de publicación MQTT determinista (`seed`, UTC base, real TLS if applicable, event IDs). Confirmar cada `received`, `accepted`, `skipped_*` count desde counters del worker y filas SQL; documentar estrategia de `latest` si se habilita, probar late samples.

## Load test
Ensayar ráfaga 10k eventos/m (ajustar umbral a hardware y documentar), con 90% sin cambios, memoria worker estable, CPU y DB writes menores que modo all en la proporción esperada. Registrar p95 ingest→current y persist lag. No inventar números máximos de capacidad sin bench.
