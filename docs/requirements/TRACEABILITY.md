# Matriz trazabilidad de requisitos

Estado inicial de TODOS los requisitos: **SPECIFIED, NOT IMPLEMENTED**. Kilo completará rutas y pruebas una vez generadas; nunca inferir PASS por existencia de una clase.

| REQ | Owner | Diseño/código | Test ID | Evidence | State |
| --- | --- | --- | --- | --- | --- |
| SYS-001 | master | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SYS-002 | infra | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SYS-003 | sandbox | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SYS-004 | db | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SYS-005 | db | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SYS-006 | config | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SYS-007 | infra | docs/plugins/… | PENDING | PENDING | BLOCKED |
| CORE-001 | identity | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-002 | projects | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-003 | assets | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-004 | semantics | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-005 | semantics | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-006 | spatial | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-007 | telemetry | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-008 | api | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-009 | events | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-010 | plugins | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-011 | plugins | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-012 | rules | docs/core/… | PENDING | PENDING | BLOCKED |
| CORE-013 | commands | docs/core/… | PENDING | PENDING | BLOCKED |
| IOT-001 | mqtt | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-002 | mqtt | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-003 | mqtt | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-004 | mqtt | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-005 | mqtt | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-006 | mqtt | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-007 | modbus | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-008 | bacnet | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-009 | http | docs/plugins/… | PENDING | PENDING | BLOCKED |
| IOT-010 | edge | docs/plugins/… | PENDING | PENDING | BLOCKED |
| BMS-001 | bms | docs/plugins/… | PENDING | PENDING | BLOCKED |
| BMS-002 | dashboards | docs/plugins/… | PENDING | PENDING | BLOCKED |
| EMS-001 | ems | docs/plugins/… | PENDING | PENDING | BLOCKED |
| EMS-002 | ems | docs/plugins/… | PENDING | PENDING | BLOCKED |
| CMMS-001 | cmms | docs/plugins/… | PENDING | PENDING | BLOCKED |
| CMMS-002 | cmms | docs/plugins/… | PENDING | PENDING | BLOCKED |
| CMMS-003 | cmms | docs/plugins/… | PENDING | PENDING | BLOCKED |
| CMMS-004 | cmms | docs/plugins/… | PENDING | PENDING | BLOCKED |
| CMMS-005 | cmms | docs/plugins/… | PENDING | PENDING | BLOCKED |
| INT-001 | erp | docs/plugins/… | PENDING | PENDING | BLOCKED |
| INT-002 | nodered | docs/plugins/… | PENDING | PENDING | BLOCKED |
| INT-003 | nodered | docs/plugins/… | PENDING | PENDING | BLOCKED |
| INT-004 | nodered | docs/plugins/… | PENDING | PENDING | BLOCKED |
| AI-001 | ai_assistant | docs/plugins/… | PENDING | PENDING | BLOCKED |
| AI-002 | mcp_server | docs/plugins/… | PENDING | PENDING | BLOCKED |
| AI-003 | mcp_server | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SEC-001 | security | docs/plugins/… | PENDING | PENDING | BLOCKED |
| SEC-002 | security | docs/plugins/… | PENDING | PENDING | BLOCKED |
| FOSS-001 | legal | docs/plugins/… | PENDING | PENDING | BLOCKED |
| FOSS-002 | legal | docs/plugins/… | PENDING | PENDING | BLOCKED |
| QA-001 | quality | docs/plugins/… | PENDING | PENDING | BLOCKED |
| QA-002 | quality | docs/plugins/… | PENDING | PENDING | BLOCKED |

## Política de seguimiento
Crear test IDs estables; registrarlos con el fixture y el gate. Cada regresión revierte estado a BLOCKED.
