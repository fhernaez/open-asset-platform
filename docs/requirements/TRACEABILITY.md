# Matriz trazabilidad de requisitos (v2 — esquema OAP-MOD-NNN)

Regenerada 2026-11-17 tras la reestructuración de `REQUIREMENTS.md`. Estados honestos: `SPECIFIED` (diseñado, sin código), `PARTIAL` (código con unit tests, sin integración real), `DONE` (aceptación real con evidencia). La integración/E2E real queda BLOCKED en sandbox y se valida en el server del usuario.

| REQ | Owner | Gate | Contrato | Código | Estado |
|---|---|---|---|---|---|
| OAP-OPS-001 | master | G1 | docs/architecture/ADR-002 | backend/ + frontend/ | PARTIAL (unit) |
| OAP-OPS-002 | infra | G1 | docs/infrastructure/DOCKER_COMPOSE.md | compose.yaml, compose.komodo.yaml | PARTIAL (config OK) |
| OAP-OPS-003 | sandbox | G1 | docs/infrastructure/VENV_AND_PYTHON.md | scripts/create_venv.sh | DONE |
| OAP-OPS-004 | db | G1 | docs/infrastructure/DB_BOOTSTRAP.md | backend/scripts/ensure_db.py | PARTIAL (unit tests) |
| OAP-OPS-005 | db | G1 | docs/infrastructure/DB_BOOTSTRAP.md | backend/scripts/ensure_db.py | PARTIAL (unit tests) |
| OAP-OPS-006 | config | G3 | docs/core/CONFIGURATION_SECRETS.md | platform.PlatformSetting | PARTIAL |
| OAP-OPS-007 | infra | G9 | docs/infrastructure/BACKUP_RESTORE_UPGRADES.md | — | SPECIFIED |
| OAP-OPS-008 | infra | G7 | docs/core/NOTIFICATIONS.md | — | SPECIFIED |
| OAP-OPS-009 | db | G1 | docs/architecture/ADR-013 | telemetry/models.py | DONE |
| OAP-PLT-001 | identity | G2 | docs/core/IDENTITY_AUTHZ.md | core/authz.py, platform | PARTIAL (unit) |
| OAP-PLT-002 | projects | G2 | docs/core/PROJECTS_TENANTS.md | platform/models.py | PARTIAL (unit) |
| OAP-PLT-003 | api | G2 | docs/contracts/REST_UI_CONTRACT.md | core/urls.py | PARTIAL |
| OAP-PLT-004 | events | G2 | docs/core/EVENTS_OUTBOX.md | events/ | PARTIAL (unit) |
| OAP-PLT-005 | plugins | G3 | docs/core/PLUGIN_MANAGER.md | plugins/ | PARTIAL (unit) |
| OAP-PLT-006 | plugins | G3 | docs/core/PLUGIN_MANAGER.md | plugins/services.py | PARTIAL (unit) |
| OAP-PLT-007 | notifications | G7 | docs/core/NOTIFICATIONS.md | — | SPECIFIED |
| OAP-PLT-008 | identity | G7 | docs/core/IDENTITY_AUTHZ.md | — | SPECIFIED |
| OAP-PLT-009 | telemetry | G6 | docs/core/TELEMETRY_POLICY.md | — | SPECIFIED |
| OAP-PLT-010 | identity | G9 | docs/core/IDENTITY_AUTHZ.md | — | SPECIFIED |
| OAP-PLT-011 | frontend | G2 | docs/architecture/ADR-016 | frontend/src/i18n/ | PARTIAL (es/en + locale por org) |
| OAP-ASS-001 | assets | G2 | docs/core/ASSET_REGISTRY.md | assets/models.py | PARTIAL (unit) |
| OAP-ASS-002 | assets | G2 | docs/core/ASSET_REGISTRY.md | assets/models.py | PARTIAL (unit) |
| OAP-ASS-003 | mqtt | G4 | docs/plugins/mqtt/SPEC.md | mqtt/models.py | PARTIAL |
| OAP-ASS-004 | assets | G6 | docs/core/ASSET_REGISTRY.md | — | SPECIFIED |
| OAP-ASS-005 | assets | G2 | docs/contracts/ASSET_TYPE_SCHEMA.md | assets/types_catalog/ | PARTIAL (~33 tipos, versionado+refresh) |
| OAP-ASS-006 | assets | G2 | docs/contracts/ASSET_TYPE_SCHEMA.md | assets/types_catalog/ | PARTIAL (seed+validator) |
| OAP-ASS-007 | assets | G2/G6 | docs/architecture/ADR-016 | frontend (iconos por categoría) | PARTIAL (iconos base) |
| OAP-TEL-001 | telemetry | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/storage.py | PARTIAL (unit) |
| OAP-TEL-002 | telemetry | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/services.py | PARTIAL (unit) |
| OAP-TEL-003 | telemetry | G6 | docs/core/TELEMETRY_POLICY.md | — | SPECIFIED |
| OAP-TEL-004 | telemetry | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/storage.py | PARTIAL (TEL-001..004 unit) |
| OAP-TEL-005 | telemetry | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/storage.py | PARTIAL (TEL-005..007 unit) |
| OAP-TEL-006 | telemetry | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/storage.py | PARTIAL (TEL-010 unit) |
| OAP-TEL-007 | telemetry | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/models.py | PARTIAL |
| OAP-TEL-008 | telemetry | G9 | docs/core/TELEMETRY_POLICY.md | — | SPECIFIED |
| OAP-SEM-001 | semantics | G6 | docs/contracts/ASSET_SEMANTIC_SCHEMA.md | — | SPECIFIED |
| OAP-SEM-002 | semantics | G6 | docs/core/SEMANTICS_81346_BRICK_HAYSTACK.md | — | SPECIFIED |
| OAP-GIS-001 | spatial | G6 | docs/contracts/SPATIAL_SCHEMA.md | — | SPECIFIED |
| OAP-GIS-002 | spatial | G6 | docs/contracts/SPATIAL_SCHEMA.md | — | SPECIFIED |
| OAP-RUL-001 | rules | G7 | docs/core/RULES_ALARMS.md | — | SPECIFIED |
| OAP-RUL-002 | commands | G7 | docs/core/ATTRIBUTES_COMMANDS.md | — | SPECIFIED |
| OAP-RUL-003 | rules | G8 | docs/core/RULES_ALARMS.md | — | SPECIFIED |
| OAP-RUL-004 | rules | G7 | docs/core/RULES_ALARMS.md | — | SPECIFIED |
| OAP-CMM-001 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-002 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-003 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-004 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-005 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-006 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-007 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-008 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-009 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-010 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-011 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-012 | cmms | G8 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-013 | cmms | G8 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-014 | cmms | G5 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-015 | cmms | G9 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-CMM-016 | cmms | G9 | docs/plugins/cmms/SPEC.md | — | SPECIFIED |
| OAP-BMS-001 | bms | G7 | docs/plugins/bms/SPEC.md | — | SPECIFIED |
| OAP-EMS-001 | ems | G7 | docs/plugins/ems/SPEC.md | — | SPECIFIED |
| OAP-EMS-002 | ems | G9 | docs/plugins/ems/SPEC.md | — | SPECIFIED |
| OAP-DSH-001 | dashboards | G6 | docs/plugins/dashboards/SPEC.md | — | SPECIFIED |
| OAP-DSH-002 | dashboards | G6 | docs/plugins/dashboards/SPEC.md | — | SPECIFIED |
| OAP-DSH-003 | dashboards | G6 | docs/plugins/dashboards/SPEC.md | — | SPECIFIED |
| OAP-CON-001 | connectivity | G4 | docs/architecture/ADR-014 | connectivity/ + assets (alta inline) | PARTIAL (unit, alta inline) |
| OAP-CON-002 | connectivity | G4 | docs/architecture/ADR-014 | connectivity/services.py | PARTIAL (unit) |
| OAP-CON-003 | connectivity | G4 | docs/plugins/mqtt/SPEC.md | connectivity/adapters/mqtt.py | PARTIAL (unit) |
| OAP-CON-004 | connectivity | G7 | docs/plugins/modbus/SPEC.md | — | SPECIFIED |
| OAP-CON-005 | connectivity | G9 | docs/plugins/protocol_extensions/SPEC.md | — | SPECIFIED |
| OAP-CON-006 | connectivity | G4 | docs/architecture/ADR-014 | connectivity/views.py | PARTIAL (UI + test-connection) |
| OAP-CON-007 | connectivity | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/storage.py + policy endpoints | PARTIAL (unit) |
| OAP-CON-008 | connectivity | G4 | docs/core/TELEMETRY_POLICY.md | telemetry/storage.py | PARTIAL (unit) |
| OAP-CON-009 | connectivity | G4 | docs/architecture/ADR-014 | connectivity/ | SPECIFIED |
| OAP-CON-010 | connectivity | G4 | docs/architecture/ADR-014 | connectivity/ | SPECIFIED |
| OAP-CON-011 | connectivity | G4 | docs/architecture/ADR-014 | connectivity/ | SPECIFIED |
| OAP-PRO-001 | modbus | G7 | docs/plugins/modbus/SPEC.md | — | SPECIFIED |
| OAP-PRO-002 | bacnet | G7 | docs/plugins/bacnet/SPEC.md | — | SPECIFIED |
| OAP-PRO-003 | http | G7 | docs/plugins/http_ws/SPEC.md | — | SPECIFIED |
| OAP-PRO-004 | edge | G7 | docs/plugins/edge/SPEC.md | — | SPECIFIED |
| OAP-PRO-005 | protocols | G9 | docs/plugins/protocol_extensions/SPEC.md | — | SPECIFIED |
| OAP-PRO-006 | protocols | G7 | docs/plugins/protocol_extensions/SPEC.md | — | SPECIFIED |
| OAP-NRD-001 | nodered | G8 | docs/contracts/NODERED_JSON.md | — | SPECIFIED |
| OAP-NRD-002 | nodered | G8 | docs/contracts/NODERED_JSON.md | — | SPECIFIED |
| OAP-NRD-003 | nodered | G8 | docs/contracts/NODERED_JSON.md | — | SPECIFIED |
| OAP-ERP-001 | erp | G8 | docs/contracts/ERP_INTEGRATION.md | — | SPECIFIED |
| OAP-AIM-001 | ai_assistant | G8 | docs/plugins/ai_assistant/SPEC.md | — | SPECIFIED |
| OAP-AIM-002 | mcp_server | G8 | docs/contracts/MCP_SECURITY.md | — | SPECIFIED |
| OAP-AIM-003 | mcp_server | G8 | docs/contracts/MCP_SECURITY.md | — | SPECIFIED |
| OAP-UI-001 | frontend | G2 | docs/contracts/REST_UI_CONTRACT.md | frontend/src/App.tsx | PARTIAL (login) |
| OAP-UI-002 | frontend | G2 | docs/contracts/REST_UI_CONTRACT.md | — | SPECIFIED |
| OAP-UI-003 | frontend | G2 | docs/contracts/REST_UI_CONTRACT.md | — | SPECIFIED |
| OAP-UI-004 | frontend | G2 | docs/quality/FRONTEND_E2E.md | — | SPECIFIED |
| OAP-UI-005 | frontend | G2-G9 | docs/plugins/*/OPERATIONS_AND_API.md | pages/{Assets,Connectivity,Telemetry,Plugins} | PARTIAL (4 pantallas reales) |
| OAP-UI-006 | frontend | G9 | docs/contracts/ASSET_TYPE_SCHEMA.md | — | SPECIFIED |
| OAP-SEC-001 | security | G9 | docs/quality/SECURITY_TESTS.md | core/permissions.py | PARTIAL |
| OAP-SEC-002 | security | G9 | docs/quality/SECURITY_TESTS.md | — | PARTIAL |
| OAP-SEC-003 | commands | G7 | docs/core/ATTRIBUTES_COMMANDS.md | — | SPECIFIED |
| OAP-QLY-001 | quality | G9 | docs/quality/QUALITY_PLAN.md | tests/ | PARTIAL |
| OAP-QLY-002 | quality | G0 | docs/quality/GATES.md | scripts/quality_gate.sh | DONE (sandbox) |
| OAP-FOSS-001 | legal | G0 | docs/legal/LICENSING_AND_CLEAN_ROOM.md | — | PARTIAL (auditoría 2026-11-17) |
| OAP-FOSS-002 | legal | G9 | docs/legal/LICENSING_AND_CLEAN_ROOM.md | — | SPECIFIED |
| OAP-FOSS-003 | legal | G0 | docs/architecture/ADR-013 | — | DONE |

## Política de seguimiento

- Crear test IDs estables; registrar fixture y gate. Cada regresión revierte a BLOCKED.
- `PARTIAL` → `DONE` solo con aceptación real (integración en PostgreSQL/Mosquitto reales, ejecutada en el server del usuario y con salida registrada en `docs/evidence/`).
- La auditoría de fuentes (2026-11-17) fija el baseline; re-auditorías actualizan `REFERENCE_LOCK.md`.
