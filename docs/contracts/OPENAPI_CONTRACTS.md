# Registro de contratos OpenAPI (Fase 1)

OpenAPI v3 es la fuente de verdad para el rebuild del frontend. El contrato del backend actual está generado y versionado en `docs/contracts/openapi.yaml` (drf-spectacular, valida con `--validate`). Los módulos futuros se especifican primero en sus `OPERATIONS_AND_API.md` y se generan al implementar su gate.

## Estado por módulo

| Módulo | Contrato fuente | OpenAPI | Estado |
|---|---|---|---|
| Platform/Identity | `docs/core/IDENTITY_AUTHZ.md`, `PROJECTS_TENANTS.md` | `openapi.yaml` (parcial) | GENERADO (actual) |
| Asset Registry | `docs/core/ASSET_REGISTRY.md` | `openapi.yaml` | GENERADO (actual) |
| Conectividad (OAP-CON) | `docs/architecture/ADR-014`, `docs/plugins/mqtt/OPERATIONS_AND_API.md` (legacy) | `openapi.yaml` (paths `/api/v1/mqtt/*` legacy) | GENERADO (actual); renombrar a `/api/v1/connectivity/*` al migrar app |
| Telemetry | `docs/core/TELEMETRY_POLICY.md` | `openapi.yaml` | GENERADO (actual) |
| Plugins | `docs/core/PLUGIN_MANAGER.md` | `openapi.yaml` | GENERADO (actual) |
| Dashboards + widget mapa | `docs/architecture/ADR-015`, `docs/plugins/dashboards/OPERATIONS_AND_API.md` | pendiente | G6 |
| GIS/Espacial | `docs/contracts/SPATIAL_SCHEMA.md` | pendiente | G6 |
| CMMS | `docs/plugins/cmms/OPERATIONS_AND_API.md` | pendiente | G5 |
| Semántica | `docs/contracts/ASSET_SEMANTIC_SCHEMA.md` | pendiente | G6 |
| Rules/Commands | `docs/core/RULES_ALARMS.md`, `ATTRIBUTES_COMMANDS.md` | pendiente | G7 |
| Protocolos/Edge | `docs/plugins/{modbus,bacnet,http_ws,edge}/OPERATIONS_AND_API.md` | pendiente | G7 |
| Node-RED | `docs/contracts/NODERED_JSON.md` | pendiente | G8 |
| ERP | `docs/contracts/ERP_INTEGRATION.md` | pendiente | G8 |
| MCP/IA | `docs/contracts/MCP_SECURITY.md` | pendiente | G8 |
| Eventos/WebSocket | `docs/contracts/EVENT_CATALOG.md` | pendiente | G2-G9 |

## Procedimiento

1. Implementar backend del módulo → exponer endpoints → regenerar `openapi.yaml`.
2. Freeze: todo cambio de contrato exige revisar la pantalla UI correspondiente y su mock MSW.
3. El frontend usa los esquemas de `openapi.yaml` + specs manuales de módulos pendientes para construir mocks MSW fieles por pantalla.
4. `REST_UI_CONTRACT.md` sigue siendo la guía de comportamiento (paginación, errores problem-details, filtros, versión `/api/v1`).
