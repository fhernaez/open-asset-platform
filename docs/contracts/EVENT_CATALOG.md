# Catálogo de eventos versionados

## Envelope común
```json
{"event_id":"uuid","event_type":"asset.attribute.observed","schema_version":"1.0","tenant_id":"uuid","project_id":"uuid","aggregate_id":"uuid","aggregate_revision":4,"occurred_at":"2026-11-13T17:00:00Z","correlation_id":"uuid","causation_id":"uuid","actor_id":"uuid-or-service","payload":{}}
```
Emitir en DB transaction outbox, consumer idempotente con `event_id`. Nunca leak token, IP interna sensible o payload personal fuera de proyecto.

## Eventos iniciales y owners
| Evento | Owner | Consumidores | Semántica |
|---|---|---|---|
| `asset.created.v1` | assets | semantic, spatial, CMMS, dashboards | identidad/metadata mínima |
| `asset.updated.v1` | assets | semantic, dashboards | revision+diff permitido |
| `asset.attribute.observed.v1` | telemetry | rules, live, alarms | TODO mensaje válido, anterior al storage filter |
| `asset.attribute.persisted.v1` | telemetry | historical analytics | solo muestra aceptada |
| `telemetry.sample.skipped.v1` | telemetry | observability | counters agregados, no 1 evento por sample si voluminoso |
| `alarm.raised.v1` | rules | notifications, CMMS | dedupe incident key |
| `alarm.cleared.v1` | rules | notifications | referencia a instancia |
| `maintenance.workorder.created.v1` | CMMS | notifications, ERP | id+status+asset refs |
| `maintenance.workorder.closed.v1` | CMMS | analytics | cost/time summary |
| `inventory.requisition.requested.v1` | inventory | ERP adapter | no orden de compra interna |
| `plugin.activation.changed.v1` | manager | workers, shell | applied/revision |
| `nodered.flow.deployed.v1` | integration | audit | hash, instance, actor |
| `mcp.proposal.approved.v1` | mcp | tool executor | approval actor + TTL |

## Evolución
Schemas JSON versionados compatibles por adición de campos opcionales; breaking changes v2 con dual publication y desuso. Contract tests para producers/consumers. Retención/auditoría separada de política de muestreo de datos; alarmas nunca se descartan por quota de telemetría.
