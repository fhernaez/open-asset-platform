# Requisitos normativos del producto (v2 — reestructurado por bounded context)

Reestructuración 2026-11-17 a partir de la auditoría de `openremote/core` @ `6d46b473` y `Grashjs/cmms` @ `06abfe35` (ver `docs/research/REFERENCE_LOCK.md` y `GRAPH_SOURCE_INDEX.md`). **MUST:** cumplir todos los IDs; el gate es puerta de aceptación, no permiso para eliminar. Cada ID se rastrea a contrato + código + prueba + evidencia en `TRACEABILITY.md`. Clasificación de fuente: `VS` VERIFIED_SOURCE, `VD` VERIFIED_DOCS_ONLY, `CU` COMMERCIAL_UNAVAILABLE, `NR` NEW_REQUIREMENT.

## Módulos

`OAP-OPS` Operaciones · `OAP-PLT` Platform/Identity · `OAP-ASS` Asset Registry · `OAP-TEL` Telemetría · `OAP-SEM` Semántica · `OAP-GIS` Espacial · `OAP-RUL` Reglas/Comandos · `OAP-CMM` CMMS · `OAP-BMS` BMS · `OAP-EMS` Energía · `OAP-DSH` Dashboards · `OAP-MQT` MQTT · `OAP-PRO` Protocolos/Edge · `OAP-NRD` Node-RED · `OAP-ERP` ERP · `OAP-AIM` IA/MCP · `OAP-UI` Frontend · `OAP-SEC` Seguridad · `OAP-QLY` Calidad · `OAP-FOSS` Legal.

## OAP-OPS — Operaciones y despliegue

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-OPS-001 | Django/React autónomo sin runtime OpenRemote/Atlas (solo referencias de auditoría) | G1 | NR |
| OAP-OPS-002 | Docker Compose desde repo GitHub con perfiles (iot), healthchecks y dependencias ordenadas | G1 | NR |
| OAP-OPS-003 | `.venv` obligatorio local antes de Python; verificado con `sys.prefix != sys.base_prefix` | G1 | NR |
| OAP-OPS-004 | Autocreación DB/roles/extensión PostGIS/migraciones en primer deploy (job db-bootstrap idempotente) | G1 | NR |
| OAP-OPS-005 | Idempotencia en volumen existente sin DB app; nunca `down -v` sin backup y consentimiento | G1 | NR |
| OAP-OPS-006 | Config env/secret/bootstrap ONCE + GUI persistida en DB; locks de deploy prevalecen | G3 | NR |
| OAP-OPS-007 | Backup/restore y upgrade comprobados con smoke real | G9 | NR |
| OAP-OPS-008 | Visor de logs del sistema con redacción de secretos | G7 | VS (OpenRemote `syslog` + page-logs) |
| OAP-OPS-009 | Base PostgreSQL plano + PostGIS (sin hypertables); TimescaleDB diferido (ADR-013) | G1 | NR |

## OAP-PLT — Platform e Identity

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-PLT-001 | Multitenancy con roles/scopes/objeto/servicio, deny-by-default | G2 | VS (OpenRemote `auth`/`security` + realms/roles pages) |
| OAP-PLT-002 | Proyectos, jerarquías y ciclo de vida | G2 | VS (Atlas locations + OpenRemote asset tree) |
| OAP-PLT-003 | REST OpenAPI versionado, filtros, paginación, WebSocket/SSE | G2 | VS (JAX-RS resources OpenRemote) |
| OAP-PLT-004 | Auditoría y outbox transaccional idempotente | G2 | VS (OpenRemote event bus + Atlas Comment/History) |
| OAP-PLT-005 | Plugins installed vs enabled, scopes y dependencias | G3 | NR |
| OAP-PLT-006 | Plugin GUI toggle con persistencia al restart; in-process sigue importado | G3 | NR |
| OAP-PLT-007 | Notificaciones (destinos, dedupe, retry) | G7 | VS (OpenRemote `notification` + Atlas NotificationController) |
| OAP-PLT-008 | Realms/organizaciones con invitación y dominios | G7 | VS (OpenRemote page-realms) |
| OAP-PLT-009 | Export de datos (datapoints, activos) | G6 | VS (OpenRemote DatapointExportFormat + page-export; Atlas ExportController) |
| OAP-PLT-010 | OIDC/SSO opcional (implementación original; SSO/LDAP de Atlas es comercial) | G9 | CU (Atlas) / NR (diseño propio) |

## OAP-ASS — Asset Registry

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-ASS-001 | Asset UUID canónico estable, tipos dinámicos, metadata, jerarquía/árbol | G2 | VS (OpenRemote Asset/AssetTree/AssetTypeInfo; Atlas Asset+Category) |
| OAP-ASS-002 | Attribute/Point esquema tipado (string/boolean/number/json) con unidad y calidad | G2 | VS (OpenRemote Attribute/MetaItem; Atlas CustomField) |
| OAP-ASS-003 | Vínculos agente↔atributo (links de protocolo) | G4 | VS (OpenRemote AttributeLink) |
| OAP-ASS-004 | Plantillas de activos y bulk import | G6 | VS (OpenRemote asset templates; Atlas ImportController) |

## OAP-TEL — Telemetría y almacenamiento

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-TEL-001 | Current value por atributo con calidad y last-valid | G4 | VS (OpenRemote AttributeState) |
| OAP-TEL-002 | Historial de datapoints con from/to y export | G4 | VS (OpenRemote Datapoint + DatapointExportFormat) |
| OAP-TEL-003 | Agregación periódica (intervalo/periodo) para consultas de gráficas | G6 | VS (OpenRemote DatapointInterval/Period + query/) |
| OAP-TEL-004 | StoragePolicy on_change por agente y por atributo (epsilon abs/rel) | G4 | NR (diferenciador OAP) |
| OAP-TEL-005 | Máximo N muestras por ventana T configurable por agente/atributo con estado durable | G4 | NR |
| OAP-TEL-006 | Dedupe/replay por source event ID, orden, UTC, calidad y resiliencia | G4 | NR |
| OAP-TEL-007 | Métricas de ingesta (received/accepted/filtered_equal/filtered_quota/invalid/duplicate/late) | G4 | NR |
| OAP-TEL-008 | Retención por ventanas vencidas (prune) | G9 | NR |

## OAP-SEM — Semántica

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-SEM-001 | IEC/ISO 81346 función/producto/ubicación con historial de designaciones | G6 | NR |
| OAP-SEM-002 | Brick/Haystack metadata, RDF proyectado y validado con SHACL | G6 | NR |

## OAP-GIS — Espacial y mapas

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-GIS-001 | Escenas por imágenes locales (planos) con capas, CRS y placement de activos | G6 | VS (OpenRemote or-map + page-map; Atlas FloorPlan) |
| OAP-GIS-002 | Geo capa MapLibre + PostGIS con overlays de estado; offline | G6 | NR (diseño propio OAP) |

## OAP-RUL — Reglas, alarmas y comandos

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-RUL-001 | Reglas declarativas (global/realm/asset) + alarmas con acknowledge/histeresis | G7 | VS (OpenRemote Ruleset/Alarms) |
| OAP-RUL-002 | Comandos seguros con interlocks y permisos explícitos | G7 | NR |
| OAP-RUL-003 | Editor de flujos declarativo (grafo de nodos) sin ejecutar lenguajes peligrosos | G8 | VS (OpenRemote Flow/Node/Wire/catalog) |
| OAP-RUL-004 | Schedules y triggers temporales | G7 | VS (OpenRemote scheduler/rules clock; Atlas Schedule) |

## OAP-CMM — Mantenimiento (paridad Atlas + mejoras OAP)

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-CMM-001 | Work requests con aprobación/rechazo/notificación + portal | G5 | VS (Atlas Request/RequestPortal) |
| OAP-CMM-002 | Work orders: estados, prioridades, asignaciones, tiempos, historial | G5 | VS (Atlas WorkOrder+History) |
| OAP-CMM-003 | Preventivo por calendario/medidor/condición con triggers de medidor | G5 | VS (Atlas PreventiveMaintenance + WorkOrderMeterTrigger) |
| OAP-CMM-004 | Checklist, adjuntos y downtime por activo | G5 | VS (Atlas Checklist/File/AssetDowntime) |
| OAP-CMM-005 | Inventario: partes, stock mínimo, movimientos, reservas | G5 | VS (Atlas Part/PartQuantity/MultiParts) |
| OAP-CMM-006 | Meters y readings con unidades | G5 | VS (Atlas Meter/Reading) |
| OAP-CMM-007 | Labor, time/cost categories, additional costs | G5 | VS (Atlas Labor/TimeCategory/CostCategory/AdditionalCost) |
| OAP-CMM-008 | Teams, turnos, permisos y contratistas | G5 | VS (Atlas Team/ShiftConfiguration/Schedule) |
| OAP-CMM-009 | Vendors y customers con historial | G5 | VS (Atlas Vendor/Customer) |
| OAP-CMM-010 | Analytics: compliance, costos, downtime, labor, reportes | G5 | VS (Atlas analytics/* + Analytics page) |
| OAP-CMM-011 | Custom fields y field configuration sin migración | G5 | VS (Atlas CustomField/FieldConfiguration/UiConfiguration) |
| OAP-CMM-012 | Workflows configurables | G8 | VS (Atlas WorkflowController) |
| OAP-CMM-013 | Import/export (fixtures y reportes) | G8 | VS (Atlas Import/Export) |
| OAP-CMM-014 | Trazabilidad histórica por activo, SLA | G5 | NR (OAP) |
| OAP-CMM-015 | Mobile/PWA responsive | G9 | VS (Atlas mobile) |
| OAP-CMM-016 | White-label/branding original (no copiar el comercial de Atlas) | G9 | CU (Atlas) |

## OAP-BMS / OAP-EMS

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-BMS-001 | HVAC, iluminación, schedules y escenas con control seguro | G7 | NR |
| OAP-EMS-001 | Medición de energía, KPIs, tarifas y reportes | G7 | NR |
| OAP-EMS-002 | Optimización y peak-shaving vía simulación/control seguro | G9 | NR |

## OAP-DSH — Dashboards e Insights

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-DSH-001 | Dashboards configurables con grid, widgets (chart/gauge/barchart/card), permisos | G6 | VS (OpenRemote Dashboard/Widget + dashboard-builder) |
| OAP-DSH-002 | Visualizador GIS embebido en dashboards | G6 | VS (OpenRemote or-map) |
| OAP-DSH-003 | Insights/analytics con muestras decimadas honestas (gap/quality) | G6 | VS (OpenRemote insights app) |

## OAP-MQT — Agente MQTT

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-MQT-001 | Broker/agente nativo: subscribe/publish/discovery, TLS/ACL | G4 | VS (OpenRemote mqtt protocol) |
| OAP-MQT-002 | Policy default on_change configurable por agente | G4 | NR |
| OAP-MQT-003 | Override por atributo con storageDatapoint=true | G4 | NR |
| OAP-MQT-004 | Máximo N valores por ventana T por agente/atributo | G4 | NR |
| OAP-MQT-005 | State y alarmas procesan cada evento antes del storage filter | G4 | NR |
| OAP-MQT-006 | Ingesta directa sin Node-RED | G4 | NR |

## OAP-PRO — Protocolos, Edge y Provisioning

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-PRO-001 | Modbus TCP/RTU lectura/escritura segura con polling | G7 | VS (OpenRemote modbus) |
| OAP-PRO-002 | BACnet/IP discovery, read/write, COV | G7 | VS (NR/adaptador propio; OpenRemote no lo incluye como adaptador listado) |
| OAP-PRO-003 | HTTP/REST/WS ingestion/polling con auth en webhooks | G7 | VS (OpenRemote http/websocket) |
| OAP-PRO-004 | Edge gateway offline spool/replay y provisioning X509 | G7 | VS (OpenRemote gateway/provisioning) |
| OAP-PRO-005 | Protocolos larga cola P2: KNX, Z-Wave, Zigbee, SNMP, TCP/UDP, LoRaWAN, Bluetooth | G9 | VS (adaptadores listados en OpenRemote) |
| OAP-PRO-006 | Simuladores por protocolo para tests | G7 | VS (OpenRemote simulator) |

## OAP-NRD — Node-RED bidireccional

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-NRD-001 | Import JSON de Node-RED → propuesta de activos/puntos con preview/commit | G8 | NR |
| OAP-NRD-002 | Export OAP → JSON flow/tab versionado sin secretos | G8 | NR |
| OAP-NRD-003 | Disparar flujos Node-RED por eventos/HTTP/MQTT | G8 | NR |

## OAP-ERP — Integración ERP

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-ERP-001 | Requisiciones OC externas con callbacks, reconciliación e idempotencia | G8 | NR (OAP reemplaza el submódulo de compras de Atlas) |

## OAP-AIM — IA local y MCP

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-AIM-001 | Asistente LLM local opt-in con RAG tenant-safe | G8 | NR |
| OAP-AIM-002 | Servidor MCP con tools/resources/prompts tipados | G8 | NR |
| OAP-AIM-003 | MCP write propose/confirm; la IA nunca controla actuadores directamente | G8 | NR |

## OAP-UI — Frontend (rebuild total)

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-UI-001 | Shell único: ruteo, design system (Ant Design), tenant/project switcher, menú RBAC | G2 | VS (OpenRemote Manager UI shell) |
| OAP-UI-002 | Pantallas completas contra contratos OpenAPI + mocks MSW | G2 | NR |
| OAP-UI-003 | Feature flags por gate: pantalla sin backend real queda oculta o "disponible en etapa X"; nunca rota | G2 | NR |
| OAP-UI-004 | E2E Playwright por pantalla (mocks y backend real por gate) | G2 | NR |
| OAP-UI-005 | Pantallas: identity/usuarios/roles, asset manager (árbol+editor), telemetría, MQTT, dashboards, GIS, reglas, CMMS, Node-RED, AI, admin | G2-G9 | VS (17 páginas OpenRemote + 21 áreas Atlas) |

## OAP-SEC — Seguridad

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-SEC-001 | RBAC/ABAC con aislamiento tenant/proyecto y deny-by-default | G9 | NR |
| OAP-SEC-002 | SSRF, CSRF, SQL/SPARQL injection, path traversal, secrets nunca en logs/GUI | G9 | NR |
| OAP-SEC-003 | Acciones peligrosas (actuadores, flows, migraciones destructivas, compras) exigen permiso explícito | G7 | NR |

## OAP-QLY — Calidad

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-QLY-001 | Unit/integration/E2E/contract/perf/security por gate con evidencia real fail-closed | G9 | NR |
| OAP-QLY-002 | Gates ejecutados con comandos reales y salida registrada; BLOCKED si falla | G0 | NR |

## OAP-FOSS — Legal

| ID | Descripción verificable | Gate | Fuente |
|---|---|---|---|
| OAP-FOSS-001 | Auditoría de licencias: no copiar código AGPLv3/comercial de Atlas ni features enterprise; solo implementaciones originales | G0 | CU (Atlas) |
| OAP-FOSS-002 | SBOM, NOTICE y reproducibilidad de releases GitHub | G9 | NR |
| OAP-FOSS-003 | Sin dependencia de TimescaleDB (TSL) — ADR-013 | G0 | VS (TSL en LICENSE.txt de OpenRemote) |

## Reglas de aceptación (sin cambio)

- `docs/requirements/TRACEABILITY.md` mapea ID → contrato → código → prueba → evidencia.
- Normas IEC/ISO requieren edición legítima; no inventar certificaciones.
- La paridad completa se logra con inventario por commit verificado (ya ejecutado 2026-11-17), no con listas de marketing.
- Cualquier requisito nuevo o incompatible exige nuevo ADR.
