# Requisitos normativos del producto

**MUST:** cumplir todos los IDs; fases indicadas son puertas de aceptación, no permiso para eliminarlos. Cada ID se rastrea a código y pruebas; capacidades de terceros no verificadas se etiquetan `TO_AUDIT`.

| ID | Descripción verificable | Gate | Owner |
| --- | --- | --- | --- |
| SYS-001 | Django/React autónomo, sin runtime OpenRemote/Atlas | G1 | master |
| SYS-002 | Docker Compose instalado desde repositorio GitHub con perfiles y health | G1 | infra |
| SYS-003 | Creación obligatoria de .venv local antes de Python | G1 | sandbox |
| SYS-004 | Autocreación DB/roles/extensiones/migraciones en primer deploy | G1 | db |
| SYS-005 | Autocreación idempotente en volumen ya existente sin DB app | G1 | db |
| SYS-006 | Configuración env/secret/bootstrap once y GUI persistida | G3 | config |
| SYS-007 | Backup/restore y upgrade comprobados | G9 | infra |
| CORE-001 | Multitenancy y roles/scopes/objeto/servicio | G2 | identity |
| CORE-002 | Proyectos, jerarquías y ciclo de vida | G2 | projects |
| CORE-003 | Asset UUID canónico y tipos dinámicos | G2 | assets |
| CORE-004 | Función-producto-ubicación y IEC/ISO 81346 historial | G6 | semantics |
| CORE-005 | Brick/Haystack mapping RDF/SHACL y ontologías | G6 | semantics |
| CORE-006 | SpatialScene imagen(es), GIS, CRS, MapLibre, offline | G6 | spatial |
| CORE-007 | Attribute/Point esquema tipado, unidad/calidad | G4 | telemetry |
| CORE-008 | REST OpenAPI, filtros, WebSocket/SSE | G2 | api |
| CORE-009 | Auditoría y outbox idempotente | G2 | events |
| CORE-010 | Plugin installed vs enabled, scopes, dependencies | G3 | plugins |
| CORE-011 | Plugin GUI toggle con persistencia al restart | G3 | plugins |
| CORE-012 | Reglas y Alarmas con acknowledge/histeresis | G7 | rules |
| CORE-013 | Comandos seguros con interlocks y permisos | G7 | commands |
| IOT-001 | MQTT Agent nativo: subscribe/publish/discovery TLS ACL | G4 | mqtt |
| IOT-002 | Agent policy default storage on_change configurable | G4 | mqtt |
| IOT-003 | Attribute storageDatapoint=true policy override on_change | G4 | mqtt |
| IOT-004 | Agent/Attribute máximo N valores por ventana T configurable | G4 | mqtt |
| IOT-005 | State + alarms procesan cada evento antes del storage filter | G4 | mqtt |
| IOT-006 | Dedup/replay, order, quality, UTC y resiliencia ingesta | G4 | mqtt |
| IOT-007 | Modbus TCP/RTU lectura escritura segura y polling | G7 | modbus |
| IOT-008 | BACnet/IP discovery, read/write, COV y polling | G7 | bacnet |
| IOT-009 | HTTP/REST/WS ingestion/polling y webhook auth | G7 | http |
| IOT-010 | Edge gateway offline spool/replay y provisioning | G7 | edge |
| BMS-001 | HVAC, lighting, schedules, scenes, controls | G7 | bms |
| BMS-002 | Dashboards configurables, widgets y visualizador GIS | G6 | dashboards |
| EMS-001 | Medición energía, KPIs, tarifas y reportes | G7 | ems |
| EMS-002 | Optimización y peak-shaving vía simulación/control seguro | G9 | ems |
| CMMS-001 | Work requests, approvals, work orders y estados | G5 | cmms |
| CMMS-002 | Mantenimiento preventivo calendario/medidor/condición | G5 | cmms |
| CMMS-003 | Tiempo, asignaciones, checklist, adjuntos, downtime | G5 | cmms |
| CMMS-004 | Repuestos, stock alert, vendor y costo técnico | G5 | cmms |
| CMMS-005 | Trazabilidad histórica por activo, SLA y reportes | G5 | cmms |
| INT-001 | ERP externo OC, callbacks, reconciliación e idempotencia | G8 | erp |
| INT-002 | Node-RED JSON → propuesta de activos/puntos | G8 | nodered |
| INT-003 | OAP → JSON flow/tab Node-RED sin secretos | G8 | nodered |
| INT-004 | Disparar flujos Node-RED por eventos/HTTP/MQTT | G8 | nodered |
| AI-001 | Asistente LLM local opt-in con RAG y permisos | G8 | ai_assistant |
| AI-002 | Servidor MCP con tools/resources/prompts tipados | G8 | mcp_server |
| AI-003 | MCP write propose/confirm y no control directo | G8 | mcp_server |
| SEC-001 | RBAC/ABAC tenant izol y deny-by-default | G9 | security |
| SEC-002 | SSRF, CSRF, SPARQL/SQL, path traversal y secrets | G9 | security |
| FOSS-001 | Auditoría licencias y features comerciales no publicadas | G0 | legal |
| FOSS-002 | SBOM, NOTICE, reproducibilidad releases GitHub | G9 | legal |
| QA-001 | Pruebas unit/integration/e2e/contract/perf/security | G9 | quality |
| QA-002 | Gates con evidencia real fail-closed | G0 | quality |

## Reglas de aceptación
- `docs/requirements/TRACEABILITY.md` mapea ID → contrato → implementación → prueba → evidencia.
- Las normas IEC/ISO requieren edición/parte adecuada; no inventar certificación sin validación externa.
- Las features Atlas solo comerciales no deben copiarse de código no accesible; implementaciones independientes permitidas.
- La paridad completa se logra con feature inventory por commit verificado, no con lista genérica de marketing.
