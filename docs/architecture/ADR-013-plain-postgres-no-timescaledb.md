# ADR: Almacenamiento de telemetría en tablas PostgreSQL regulares (sin TimescaleDB)

Estado: **Aceptada** (2026-11-17).

## Contexto

TimescaleDB se adoptó inicialmente por inspiración de OpenRemote. Sin embargo, la política de persistencia `on_change` + `max_samples N/ventana T` filtra la mayor parte de los eventos antes de escribir, por lo que el volumen persistido es moderado y no justifica el costo de hypertables.

Además, el intento de convertir `telemetry_telemetrypoint` en hypertable falló con `cannot create a unique index without the column "ts" (used in partitioning)`: TimescaleDB exige que la columna de tiempo esté presente en todo índice único y en la primary key, mientras que Django 6.0 no soporta claves primarias compuestas (verificado: `CompositePrimaryKey` no existe en el paquete instalado). Esta incompatibilidad es estructural, no un bug puntual.

## Decisión

Usar **tablas PostgreSQL regulares** para telemetría (sin hypertables), manteniendo **PostGIS** para lo espacial:

- `TelemetryPoint`: primary key `id` autoincremental + índice B-tree `(attribute_id, ts DESC)` + restricción única `(attribute_id, dedupe_key)`.
- Retención por borrado de ventanas vencidas (comando `prune_telemetry` en el worker), no por `drop_chunks`.
- Particionado nativo de PostgreSQL (por mes) queda como opción de escalado futuro, no como dependencia.

## Consecuencias

- Se elimina el management command `ensure_hypertables` y la dependencia de la imagen `timescaledb-ha`; la imagen de DB es `postgis/postgis`.
- El bootstrap instala solo `postgis` (`DB_REQUIRED_EXTENSIONS=postgis`).
- TimescaleDB queda diferido: se reevaluará solo si el volumen medido lo justifica, y en ese caso se resolverá la clave compuesta (tabla `managed=False` o ingesta fuera del ORM).

## Alternativas consideradas

- `django-timescaledb`: agrega dependencia de terceros y no resuelve el conflicto de clave compuesta. Rechazado.
- Particionado nativo: requiere igualmente que PK/unique incluyan la columna de partición. Diferido.
- Índice BRIN sobre `ts`: no aplica al patrón de consulta dominante (`attribute_id` UUID aleatorio). Complementario, no sustituto.
- MongoDB/FerretDB/DocumentDB: modelo documental peor ajustado a telemetría tipada; FerretDB es Postgres por debajo. Rechazado.

## Referencias internas

- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/architecture/DB_LOGICAL_MODEL.md`
- `docs/infrastructure/DB_BOOTSTRAP.md`
- `docs/core/TELEMETRY_POLICY.md`
