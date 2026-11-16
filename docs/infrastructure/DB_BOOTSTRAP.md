# DB-B001 — Aprovisionamiento automático PostgreSQL/TimescaleDB/PostGIS

**Requisito bloqueante:** `docker compose up -d --build` debe crear la base de datos requerida si no existe, sin pasos SQL manuales, ejecutar extensiones/migraciones y dejar servicios saludables. Probar tanto volumen nuevo como volumen antiguo sin la BD OAP. La inicialización NO puede destruir información preexistente.

## 1. No confundir dos mecanismos
1. La imagen PostgreSQL ejecuta `/docker-entrypoint-initdb.d/` SÓLO cuando PGDATA está vacío. `POSTGRES_DB` puede crear la DB en primer cluster init, pero no cuando un volumen preexistente carece de esa DB.
2. OAP incluye un `db-bootstrap` **one-shot service** idempotente que se conecta al DB admin (a DB `postgres`), consulta `pg_database` y crea role/db si faltan con SQL seguro, luego valida/extiende la DB OAP. Se ejecuta aun con volumen ya inicializado. NO montar socket Docker ni dar privilegios admin a Django API.

## 2. Pipeline Compose y dependencias
```yaml
services:
  db:
    # Imagen aprobada TimescaleDB+PostGIS; version/digest fijar en release
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d postgres"]
  db-bootstrap:
    # imagen ligera con psql, secrets de admin, script /app/db/ensure-db.sh
    depends_on:
      db:
        condition: service_healthy
    restart: "no"
  migrate:
    # imagen backend; SOLO migraciones versionadas, no makemigrations en prod
    depends_on:
      db-bootstrap:
        condition: service_completed_successfully
    command: ["python", "manage.py", "migrate", "--noinput"]
    restart: "no"
  api:
    depends_on:
      migrate:
        condition: service_completed_successfully
```
Esta estructura es especificación: Kilo debe generar `compose.yaml` concreto y validarlo con `docker compose config`, sin dejar placeholders `# image` sin resolver en runtime.

## 3. Algoritmo del job db-bootstrap
- Leer `DB_ADMIN_PASSWORD_FILE`, `DB_APP_PASSWORD_FILE` de Docker secrets, validar `DB_NAME/DB_USER` como identificadores permitidos, usar `psql -v ON_ERROR_STOP=1` y quoting seguro de identifiers/literals (no concatenación insegura).
- Esperar readiness con timeout fijo y backoff; usar advisory lock en DB `postgres` para evitar inicializaciones paralelas y asegurar idempotencia. Recordar `CREATE DATABASE` no permite ejecutarse dentro de bloque de transacción; diseñar locking externo o lock de sesión/serialización apropiada y comprobar `pg_database` justo antes, nunca intentar transaction wrapping incorrecto.
- Crear role si falta con LOGIN/least privileges y secret, crear DB con OWNER role si falta; si existen, verificar owner/encoding y reportar conflicto sin DROP.
- Conectar a DB app, `CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS timescaledb;` con imagen que realmente las incluya; verificar `pg_extension` y versiones. Si falla extensión, job FAIL y API no levanta; no fallback silencioso a PostgreSQL sin Timescale.
- Crear schema `core`, `telemetry`, `plugins` si diseño lo requiere y privilegios mínimos; evitar que superuser opere API.
- Service migrator ejecuta `python manage.py migrate --noinput` y `bootstrap_config --seed-missing-only`; usa lock y no destruye plugins settings existentes.
- En first boot, administrador local inicial se crea mediante secret bootstrap o flujo seguro de invitación. Nunca `admin/admin`.

## 4. Persistencia y recuperación
- `docker compose down` conserva volumen; `down -v` destructivo prohibido sin backup/consentimiento.
- Restart, rebuild y upgrade no deben recrear DB ni sobrescribir configuración administrable.
- No `makemigrations` en startup de producción. Siempre commit migration files y revisar expand/contract.
- Backups con `pg_dump -Fc` y estrategias para Timescale/roles/extensiones probadas; recuperar en contenedor staging y ejecutar smoke real.

## 5. Casos de prueba de aceptación DB-B001
1. **Volumen vacío:** `docker compose down` (no -v), crear nuevo nombre de proyecto y nuevo volume para test, `docker compose up -d --build` → DB/roles/extensiones/tabla migrations existen, API healthy, login disponible.
2. **Idempotencia:** repetir `up`, `restart` 3 veces → mismos records, settings, rows, DB sin duplicación.
3. **Volumen existente sin DB app:** crear volumen con cluster válido pero sin DB `oap`, iniciar stack → job crea DB y migra; otros DB del cluster no se tocan.
4. **Dos bootstraps concurrentes:** no duplicate/db race, ambos terminan safe o uno espera.
5. **Extensión ausente:** job failure no API green; log claro y sanitizado.
6. **Permisos mínimos:** API DB user no puede `CREATE DATABASE`, admin secret no está en API env/log.
7. **Upgrade:** migración aditiva sobre datos existentes conserva activos, plugin states, telemetry histories.
8. **Restore:** restaurar backup de staging y verificar cantidades, extensión, consultas hypertable, permisos, web.

## 6. Referencias
Docker Postgres guide: `https://docs.docker.com/guides/postgresql/` (init scripts solo PGDATA vacío). Docker Compose dependencies: `https://docs.docker.com/compose/how-tos/startup-order/` (service_healthy y completed_successfully). Revisar versiones/soporte de PostgreSQL con extensión Timescale instalada, no asumir compatible con cualquier PG mayor.
