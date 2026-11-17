# Baselines de repositorios y estándares — fijar antes de implementar paridad

## Registro obligatorio

| name | remote_url | commit | date_utc | license_spdx | paths_audited | reviewed_by |
|---|---|---|---|---|---|---|
| openremote/core | https://github.com/openremote/core | `6d46b473d353533ccfc3938956eed145a134f2d8` | 2026-11-16 (commit); 2026-11-17 (auditoría) | CDDL-1.0 + GPL-2.0-only (Classpath exception) + Timescale TSL + terceros (`LICENSE.txt`) | `settings.gradle`, `agent/src/main/java/org/openremote/agent/protocol/` (19 adaptadores), `manager/src/main/java/org/openremote/manager/` (24 servicios), `model/src/main/java/org/openremote/model/` (30 dominios), `ui/app/manager/src/pages/` (17 páginas), `ui/component/` | kilo-code-agent |
| Grashjs/cmms (Atlas CMMS) | https://github.com/Grashjs/cmms | `06abfe35d09372ff80f889fcde73eb3cc71dc205` | 2026-11-05 (commit); 2026-11-17 (auditoría) | AGPL-3.0 (open) + Comercial dual (INTELLOOP LLC, `COMMERCIAL_LICENSE.MD`) | `api/src/main/java/com/grash/controller/` (66 controllers), `.../model/` (50+ entidades), `frontend/src/content/pages/` (21 áreas), `service/LicenseService.java`, `README.MD` | kilo-code-agent |

Notas de auditoría (2026-11-17):
- OpenRemote `LICENSE.txt` incluye el **Timescale License Agreement (TSL)**: confirma que la dependencia de TimescaleDB en OpenRemote está bajo TSL (source-available, no OSI). OAP la evita por diseño (ADR-013).
- Atlas CMMS es **dual-licensed**: el repo público es AGPLv3; white-labeling, branding custom, SSO, LDAP y "enterprise features" requieren `LICENSE_KEY` (comercial). OAP implementa solo implementaciones originales de las capacidades; no copia código comercial no publicado.
- Los commits fijados arriba son los puntos de comparación; cualquier re-auditoría debe actualizar este registro.

## Estándares y docs (sin cambio)

- `https://kilo.ai/docs/customize/agents-md`, `.../custom-rules`, `.../workflows`, `.../custom-modes`: rutas Kilo documentadas a noviembre 2026.
- `https://docs.djangoproject.com/en/5.2/` — documentación Django 5.2 LTS; confirmar versiones soportadas antes de instalar.
- `https://docs.docker.com/guides/postgresql/` — init scripts solo con directorio de datos vacío.
- `https://docs.docker.com/compose/how-tos/startup-order/` — service_healthy y service_completed_successfully.
- `https://docs.brickschema.org/`, `https://www.project-haystack.org/`, IEC/ISO 81346 (norma con copyright, obtener legítimamente), GeoSPARQL, SHACL, W3C RDF.
- `https://nodered.org/docs/api/admin/methods/` — Admin API de Node-RED para import/export de flows.
- `https://modelcontextprotocol.io/specification/` — MCP.

## Advertencia funcional

Las limitaciones de OpenRemote sobre on-change y límite N/T son **observaciones de uso planteadas por el usuario** que OAP DEBE resolver (verificadas como requisitos propios `NEW_REQUIREMENT`, no como conclusión sobre todas las versiones de OpenRemote). Ver `docs/research/GRAPH_SOURCE_INDEX.md` para el inventario por paths.
