# Baselines de repositorios y estándares — fijar antes de implementar paridad

## Registro obligatorio

| name | remote_url | commit | date_utc | license_spdx | paths_audited | reviewed_by |
|---|---|---|---|---|---|---|
| openremote/core | https://github.com/openremote/core | `6d46b473d353533ccfc3938956eed145a134f2d8` | 2026-11-16 (commit); 2026-11-17 (auditoría) | CDDL-1.0 + GPL-2.0-only (Classpath exception) + Timescale TSL + terceros (`LICENSE.txt`) | `settings.gradle`, `agent/src/main/java/org/openremote/agent/protocol/` (19 adaptadores), `manager/src/main/java/org/openremote/manager/` (24 servicios), `model/src/main/java/org/openremote/model/` (30 dominios), `ui/app/manager/src/pages/` (17 páginas), `ui/component/` | kilo-code-agent |
| Grashjs/cmms (Atlas CMMS) | https://github.com/Grashjs/cmms | `06abfe35d09372ff80f889fcde73eb3cc71dc205` | 2026-11-05 (commit); 2026-11-17 (auditoría) | AGPL-3.0 (open) + Comercial dual (INTELLOOP LLC, `COMMERCIAL_LICENSE.MD`) | `api/src/main/java/com/grash/controller/` (66 controllers), `.../model/` (50+ entidades), `frontend/src/content/pages/` (21 áreas), `service/LicenseService.java`, `README.MD` | kilo-code-agent |
| thingsboard/thingsboard | https://github.com/thingsboard/thingsboard | `80c1c615651f100a7297b62da2d488127e158990` | 2026-11-17 (auditoría) | **BUSL-1.1** (source-available; producción libre dentro del grant; branding/comercial requiere licencia). **Solo referencia de patrones; NO copiar código** | `application/src/main/java/org/thingsboard/server/controller/` (Agent/Profile, Asset/Profile, Device/Profile, ConverterLibrary, RuleChain, WidgetsBundle/WidgetType, Telemetry, Alarm, Tenant/Profile, Edge, WhiteLabeling, Trendz), `README.md`, `LICENSE` | kilo-code-agent |
| edgexfoundry/edgex-compose | https://github.com/edgexfoundry/edgex-compose | `7336ef74a17a952edb5280e8f4b42e7a86c2acd5` | 2026-11-17 (auditoría) | Apache-2.0 | `docker-compose.yml` (core-data/metadata/command/keeper, app-rules-engine, support-notifications/scheduler, ui, kuiper, mqtt-bus, device-rest, device-virtual) | kilo-code-agent |
| edgexfoundry/device-mqtt-go | https://github.com/edgexfoundry/device-mqtt-go | `4a4ecfa4ee56ff00ee1b778d6438b68c2f479101` | 2026-11-17 (auditoría) | Apache-2.0 | estructura device service (cmd/, internal/driver) | kilo-code-agent |
| edgexfoundry/device-modbus-go | https://github.com/edgexfoundry/device-modbus-go | `36976fffdbfa192c834a01c0726c86c0ce9ab046` | 2026-11-17 (auditoría) | Apache-2.0 | estructura device service | kilo-code-agent |
| edgexfoundry/device-rest-go | https://github.com/edgexfoundry/device-rest-go | `e06f0096ab872ae9652e97bb7200963bcd49c1be` | 2026-11-17 (auditoría) | Apache-2.0 | estructura device service | kilo-code-agent |
| edgexfoundry/device-virtual-go | https://github.com/edgexfoundry/device-virtual-go | `51a4860f7a496206684d7bc404f1c64d674ea9c4` | 2026-11-17 (auditoría) | Apache-2.0 | estructura device service | kilo-code-agent |
| edgexfoundry/device-snmp-go | https://github.com/edgexfoundry/device-snmp-go | `979eae0b6990b875aee90110b430c1afa4f8de39` | 2026-11-17 (auditoría) | Apache-2.0 | estructura device service | kilo-code-agent |
| node-red/node-red | https://github.com/node-red/node-red | `f613ba109eff360a1c8f8cb9add7b39531c75f12` | 2026-11-17 (auditoría) | Apache-2.0 | `packages/node_modules/@node-red/nodes/core/` (common, function, network: mqtt/http/ws/tcp/udp/tls, parsers, sequence, storage) | kilo-code-agent |
| grafana/grafana | https://github.com/grafana/grafana | `f0b5ff912d88d4592600980c44ac27739a373f75` | 2026-11-17 (auditoría) | **AGPL-3.0**. **Solo referencia de patrones; NO copiar código** | `public/app/plugins/panel/` (30 paneles: timeseries, gauge, stat, barchart, table, canvas, geomap, state-timeline, status-history, nodeGraph, heatmap…) | kilo-code-agent |

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
