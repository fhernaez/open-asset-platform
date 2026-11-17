# Definition of Done por historia y release

## Historia
- Contrato funcional y requisitos identificados con ID.
- Migración reversible o plan expand/contract, índice/constraints y tenant isolation.
- API + UI visible si aplica; error/empty/loading state; authz y audit.
- Tests positivos, negativos, concurrencia, restart/replay cuando aplique.
- PR code review independiente, docs actualizadas, no secret.
- Evidencia comando + exit code + fixture + logs reales, QA firmó PASS. No tests skipeados sin bloqueo.

## Hito
- Todos los acceptance IDs de etapa PASS en Compose de test contra PostgreSQL/PostGIS reales.
- Smoke E2E con frontend real, health, no cambios de schema fuera de migraciones.
- Riesgos/limitaciones documentados y aprobados para siguiente etapa.

## Release
- Backup/restauración verificada, rollback plan, SBOM/licencias, imagen reproducible, lock, security scanner, plugin matrix, no dependencia de OpenRemote/Atlas, no Node-RED requerido para MQTT.
- Paridad comercial/fuente y hardware no declaradas salvo evidencia adicional.
