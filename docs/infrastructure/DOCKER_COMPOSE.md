# Docker Compose como distribución principal

## Servicios y perfiles
| Servicio | Perfil | Función |
|---|---|---|
| `db` | base | PostgreSQL/PostGIS con volumen persistente |
| `db-bootstrap` | base | role/DB/extensiones idempotente, one-shot |
| `migrate` | base | Django migraciones + seed de defaults, one-shot |
| `api` | base | Django/DRF endpoints+auth+admin |
| `frontend` | base | React build y proxy estático |
| `event-worker` | base | outbox/notifications jobs |
| `mqtt-broker` | iot | Mosquitto u otro FOSS aprobado, ACL+TLS |
| `telemetry-worker` | iot | ingest, current/rules, storage policy, TSDB |
| `rules-worker` | automation | schedules/alarms/commands |
| `semantic-worker` | semantic | RDF projection/SHACL |
| `mcp-server` | mcp | MCP auth+tools, no DB raw |
| `ai-runner` | ai | LLM adapter opcional, no GPU mandatory |
| `nodered` | optional-nodered | servicio independiente, NO requisito para MQTT |
| `identity` | oidc | OIDC Keycloak opcional (auth base segura) |

## Roles de datos
Only db-bootstrap holds DB admin secret, api/migrate uses app-specific secret. No Internet outbound required for operation normal salvo integrations opt-in. Nginx/reverse proxy TLS with headers CSP/HSTS, restricted CORS. Database and broker ports NOT published in producción salvo política explícita.

## Startup
`db service_healthy` → `db-bootstrap completed_successfully` → `migrate completed_successfully` → `api/worker` → frontend. Timeout/retry y health/readiness. `.env.example` documenta perfiles y valores no sensibles; `secrets/*.txt` no versionados, production secret manager opt-in.

## Build
Dockerfiles multi-stage, Python/Node pinned versions, no dev server Django en producción, static assets versionados, user non-root para api/workers, read-only fs cuando sea viable, volumes persistentes DB/uploads, healthcheck y resource limits. No bajar `latest` en releases; incluir SBOM y licencia.

## Tests
`docker compose config --quiet`, `docker compose build`, `up` con volumen fresco, DB-bootstrap, migraciones, API GET health, frontend/login, mqtt direct, restart `down`/`up` conserva preferencias y telemetry; `existing-volume-without-db` caso obligatorio. `docker compose down -v` sólo en proyecto de pruebas aislado y explícitamente autorizado.
