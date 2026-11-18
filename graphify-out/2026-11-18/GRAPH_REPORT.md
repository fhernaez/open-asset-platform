# Graph Report - Open-Asset-Platform  (2026-11-18)

## Corpus Check
- 369 files · ~113,158 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 5, .example 2, .conf 2)

## Summary
- 2409 nodes · 3283 edges · 297 communities (214 shown, 83 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `10f1b002`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- connectivity_worker.py
- PluginManager
- package.json
- platforms/views.py
- assets/views.py
- django_db
- ensure_db.py
- conftest.py
- errors.py
- core/views.py
- App.tsx
- ConnectivityPage.tsx
- compilerOptions
- devDependencies
- compilerOptions
- manifest.json
- tsconfig.json
- G1.sh
- G2.sh
- G3.sh
- G4.sh
- quality_gate.sh
- create_venv.sh
- gen_dev_secrets.sh
- ValidationError
- AuthProvider.tsx
- mqtt.py
- AppContext.tsx
- oap-backend
- apiFetch
- TenantScopedPermission
- AssetType
- telemetry/models.py
- Requisitos normativos del producto (v2 — reestructurado por bounded context)
- json
- test_telemetry_policy.py
- Gateway
- Arquitectura maestra — OAP autonomous FOSS
- Plan de construcción secuencial para Kilo Code — NO crear todos los plugins de una vez
- Backlog estructurado de funcionalidades — v3 (2026-11-17)
- `cmms` — Operaciones paso a paso, API, UX y fallas
- `nodered` — Operaciones paso a paso, API, UX y fallas
- `ai_assistant` — Operaciones paso a paso, API, UX y fallas
- Plugin `ai_assistant` — especificación funcional y técnica
- Plugin `analytics` — especificación funcional y técnica
- Plugin `bacnet` — especificación funcional y técnica
- `bms` — Operaciones paso a paso, API, UX y fallas
- Plugin `bms` — especificación funcional y técnica
- Plugin `cmms` — especificación funcional y técnica
- Plugin `dashboards` — especificación funcional y técnica
- Plugin `edge` — especificación funcional y técnica
- `ems` — Operaciones paso a paso, API, UX y fallas
- Plugin `ems` — especificación funcional y técnica
- Plugin `erp` — especificación funcional y técnica
- `http_ws` — Operaciones paso a paso, API, UX y fallas
- Plugin `http_ws` — especificación funcional y técnica
- Plugin `inventory` — especificación funcional y técnica
- `mcp_server` — Operaciones paso a paso, API, UX y fallas
- Plugin `mcp_server` — especificación funcional y técnica
- Plugin `modbus` — especificación funcional y técnica
- `mqtt` — Operaciones paso a paso, API, UX y fallas
- Plugin `mqtt` — especificación funcional y técnica
- Plugin `nodered` — especificación funcional y técnica
- Plugin `protocol_extensions` — especificación funcional y técnica
- ingest_event
- CONTRATO NORMATIVO — Telemetría MQTT: persistir por cambio y máximo N valores/período
- `analytics` — Operaciones paso a paso, API, UX y fallas
- `bacnet` — Operaciones paso a paso, API, UX y fallas
- `dashboards` — Operaciones paso a paso, API, UX y fallas
- `edge` — Operaciones paso a paso, API, UX y fallas
- `erp` — Operaciones paso a paso, API, UX y fallas
- `inventory` — Operaciones paso a paso, API, UX y fallas
- `modbus` — Operaciones paso a paso, API, UX y fallas
- Escenarios específicos obligatorios
- `protocol_extensions` — Operaciones paso a paso, API, UX y fallas
- django_apps
- AssetAttribute
- CORE / Api Realtime
- CORE / Asset Registry
- CORE / Attributes Commands
- CORE / Configuration Secrets
- CORE / Dashboards Ui
- CORE / Edge Provisioning
- CORE / Events Outbox
- CORE / Identity Authz
- CORE / Notifications
- CORE / Plugin Manager
- CORE / Projects Tenants
- CORE / Rules Alarms
- CORE / Semantics 81346 Brick Haystack
- CORE / Spatial Scenes
- Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE
- Escenarios específicos obligatorios
- mockServiceWorker.js
- platforms/admin.py
- OAP — Instrucciones vinculantes para cualquier agente de Kilo Code
- ConfigService
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Escenarios específicos obligatorios
- Recorridos Playwright E2E de aplicación
- Contrato de sandbox local, Docker y herramientas
- ADR: Framework Django como core, no FastAPI
- ADR: Producto independiente
- ADR: Módulos estables y addons administrables
- ADR: Single source of truth y propiedad
- ADR: Almacenamiento MQTT selectivo
- ADR: IEC/ISO 81346 + Brick + Haystack
- ADR: SpatialScene multiproyecto
- ADR: Seguridad de control físico
- ADR: Bootstrap automático PostgreSQL
- ADR: MCP y asistente local desacoplados
- ADR: ERP y Node-RED como externos
- ADR: Licenciamiento verificable
- Contrato de configuración ENV / DB / GUI
- DB-B001 — Aprovisionamiento automático PostgreSQL/PostGIS
- Pruebas de contratos: REST, eventos, plugins, RDF, UI y MCP
- Fixtures de QA sintéticas
- dependencies
- scripts
- OAP — Open Asset Platform | Especificación integral para Kilo Code
- TelemetryPage.tsx
- telemetry/views.py
- endpoints.ts
- OutboxEvent
- Manual de orquestación Kilo Code: agentes, tareas y checkpoints
- ADR: Almacenamiento de telemetría en tablas PostgreSQL regulares (sin TimescaleDB)
- Diagramas de flujo C4 lógico + escenarios operativos
- Contrato de identidad, activos, IEC 81346 y RDF
- Node-RED JSON bidireccional, modelo de negociación y export de pestaña
- Contrato espacial — GIS/planos/escenas
- Esquema de telemetría y políticas de almacenamiento
- Docker Compose como distribución principal
- Variables de entorno OAP — esquema, defaults, administración
- Rendimiento y observabilidad
- Pruebas de seguridad negativas — por ruta/protocolo
- Extracción de grafo de código de repositorios de referencia
- Contexto persistente para Kilo Code: Open Asset Platform
- Modelo lógico SQL y owners
- REST, realtime y frontend plugin contract
- Operación: backup, restauración y upgrades
- GitHub CI, PR, releases y calidad de supply chain
- Python .venv — instrucciones obligatorias para agentes
- `ai_assistant` — Esquema de datos, constraints y migraciones
- `analytics` — Esquema de datos, constraints y migraciones
- `bacnet` — Esquema de datos, constraints y migraciones
- `bms` — Esquema de datos, constraints y migraciones
- `cmms` — Esquema de datos, constraints y migraciones
- `dashboards` — Esquema de datos, constraints y migraciones
- `edge` — Esquema de datos, constraints y migraciones
- `ems` — Esquema de datos, constraints y migraciones
- `erp` — Esquema de datos, constraints y migraciones
- `http_ws` — Esquema de datos, constraints y migraciones
- `inventory` — Esquema de datos, constraints y migraciones
- `mcp_server` — Esquema de datos, constraints y migraciones
- `modbus` — Esquema de datos, constraints y migraciones
- `mqtt` — Esquema de datos, constraints y migraciones
- `nodered` — Esquema de datos, constraints y migraciones
- `protocol_extensions` — Esquema de datos, constraints y migraciones
- Estrategia de verificación independiente
- Funcionalidad a partir de fuentes (auditoría ejecutada 2026-11-17)
- Integración ERP por requisición técnica
- Catálogo de eventos versionados
- Política de licencias FOSS, ingeniería limpia y publicación GitHub
- Plugin manifest — `ai_assistant`
- Plugin manifest — `analytics`
- Plugin manifest — `bacnet`
- Plugin manifest — `bms`
- Plugin manifest — `cmms`
- Plugin manifest — `dashboards`
- Plugin manifest — `edge`
- Plugin manifest — `ems`
- Plugin manifest — `erp`
- Plugin manifest — `http_ws`
- Plugin manifest — `inventory`
- Plugin manifest — `mcp_server`
- Plugin manifest — `modbus`
- Plugin manifest — `mqtt`
- Plugin manifest — `nodered`
- Plugin manifest — `protocol_extensions`
- Definition of Done por historia y release
- Índice de fuentes auditadas (2026-11-17)
- Baselines de repositorios y estándares — fijar antes de implementar paridad
- SYSTEM — Principal para agentes de construcción OAP
- Cómo interpretar “reconstruir todas las funcionalidades”
- Registro de contratos OpenAPI (Fase 1)
- Aceptación del plugin `ai_assistant` — G8
- Aceptación del plugin `analytics` — G9
- Aceptación del plugin `bacnet` — G7
- Aceptación del plugin `bms` — G7
- Aceptación del plugin `cmms` — G5
- Aceptación del plugin `dashboards` — G6
- Aceptación del plugin `edge` — G7
- Aceptación del plugin `ems` — G7
- Aceptación del plugin `erp` — G8
- Aceptación del plugin `http_ws` — G7
- Aceptación del plugin `inventory` — G5
- Aceptación del plugin `mcp_server` — G8
- Aceptación del plugin `modbus` — G7
- Aceptación del plugin `mqtt` — G4
- Aceptación del plugin `nodered` — G8
- Aceptación del plugin `protocol_extensions` — G9
- Puertas de calidad G0–G9 — fail-closed
- Casos deterministas para almacenar solo cambios y máximo N/T
- Grafo de dependencias planificado (NO grafo extraído del código fuente)
- Matriz trazabilidad de requisitos (v2 — esquema OAP-MOD-NNN)
- architecture-auditor
- devops
- django-core
- frontend-ux
- iot-telemetry
- oap-lead
- plugin-integrations
- quality-security
- semantics-spatial
- CONTRIBUTING.md
- FAILURE_RECOVERY.md
- TEST_EVIDENCE_TEMPLATE.md
- IMPLEMENTATION_STORY_TEMPLATE.md
- MVP_USER_JOURNEY.md
- DB_BOOTSTRAP_CASES.md
- PARITY_ATLAS.md
- PARITY_OPENREMOTE.md
- VERIFIED_PUBLIC_REFERENCES.md
- START_HERE.md
- oap-audit.md
- oap-build-all.md
- oap-next.md
- oap-release.md
- oap-start.md
- oap-telemetry.md
- oap-validate.md
- 01-sandbox.md
- 02-architecture.md
- 03-data.md
- 04-foss.md
- 05-qa.md
- 06-ui.md
- 07-agent-safety.md
- prompts/CONTEXT.md
- INITIAL_USER_PROMPT.md
- Patrones extraídos de repos de referencia (2026-11-17)
- ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes
- connectivity/views.py
- connectivity/services.py
- browser.ts
- API MCP — permisos y aprobación
- Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1)
- ADR: Representación visual de activos e i18n estructural
- connectivity/admin.py
- index.ts
- msw
- @testing-library/jest-dom

## God Nodes (most connected - your core abstractions)
1. `apiFetch()` - 38 edges
2. `Gateway` - 27 edges
3. `AssetType` - 23 edges
4. `AssetAttribute` - 23 edges
5. `TenantScopedPermission` - 23 edges
6. `ValidationError` - 22 edges
7. `Membership` - 22 edges
8. `ingest_event()` - 22 edges
9. `Requisitos normativos del producto (v2 — reestructurado por bounded context)` - 22 edges
10. `Asset` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Scopes` --references--> `AuthzService`  [INFERRED]
  docs/contracts/MCP_SECURITY.md → backend/core/authz.py
- `Integridad` --references--> `StoragePolicyState`  [INFERRED]
  docs/architecture/DB_LOGICAL_MODEL.md → backend/telemetry/models.py
- `Estados y métricas` --references--> `AttributeCurrent`  [INFERRED]
  docs/contracts/TELEMETRY_SCHEMA.md → backend/telemetry/models.py
- `Bitácora de tareas verificables` --references--> `StoragePolicyState`  [INFERRED]
  docs/evidence/TASK_LOG.md → backend/telemetry/models.py
- `6. Datos que deben almacenarse` --references--> `AttributeCurrent`  [INFERRED]
  docs/core/TELEMETRY_POLICY.md → backend/telemetry/models.py

## Import Cycles
- None detected.

## Communities (297 total, 83 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.14
Nodes (10): canonical_json(), is_change(), merge_policy(), normalize_value(), parse_window(), utcnow(), window_bucket(), _apply_policy() (+2 more)

### Community 2 - "PluginManager"
Cohesion: 0.07
Nodes (28): ConflictError, Command, PluginActivationAdmin, PluginDefinitionAdmin, PluginInstallationAdmin, PluginSettingsAdmin, Kind, Meta (+20 more)

### Community 3 - "package.json"
Cohesion: 0.10
Nodes (21): name, private, type, version, echarts, eslint, @eslint/js, eslint-plugin-react-hooks (+13 more)

### Community 4 - "platforms/views.py"
Cohesion: 0.16
Nodes (19): UUIDPkModel, AuditLog, Membership, Meta, PlatformSetting, Project, Tenant, TenantScopedModel (+11 more)

### Community 5 - "assets/views.py"
Cohesion: 0.15
Nodes (16): AssetAdmin, AssetAttributeAdmin, AssetRelationshipAdmin, AssetTypeAdmin, UnitAdmin, Asset, AssetRelationship, Meta (+8 more)

### Community 6 - "django_db"
Cohesion: 0.12
Nodes (11): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+3 more)

### Community 7 - "ensure_db.py"
Cohesion: 0.06
Nodes (13): _read_secret(), _create_database(), _create_role(), _env(), _install_extensions(), main(), _read_secret(), _validate_identifier() (+5 more)

### Community 8 - "conftest.py"
Cohesion: 0.06
Nodes (27): RoleAdmin, UserAdmin, Meta, Role, TimeStampedModel, User, UserManager, request_context() (+19 more)

### Community 9 - "errors.py"
Cohesion: 0.11
Nodes (12): AssetService, AttributeService, AuthzService, api_exception_handler(), DependencyUnavailableError, NotFoundError, OAPError, PermissionDeniedError (+4 more)

### Community 10 - "core/views.py"
Cohesion: 0.10
Nodes (8): StandardPagination, Meta, TokenObtainPairSerializer, UserSerializer, HealthView, LoginView, MeView, RefreshView

### Community 11 - "App.tsx"
Cohesion: 0.16
Nodes (22): ADR-0014, createProject(), createTenant(), listProjects(), App(), IMPLEMENTED_PAGES, ProtectedLayout(), screenElement() (+14 more)

### Community 12 - "ConnectivityPage.tsx"
Cohesion: 0.26
Nodes (11): createBinding(), createGateway(), deleteBinding(), deleteGateway(), listAssets(), listAttributes(), listBindings(), BindingsDrawer() (+3 more)

### Community 13 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleDetection, moduleResolution (+9 more)

### Community 14 - "devDependencies"
Cohesion: 0.11
Nodes (18): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, msw (+10 more)

### Community 15 - "compilerOptions"
Cohesion: 0.18
Nodes (10): compilerOptions, allowSyntheticDefaultImports, lib, module, moduleResolution, noEmit, skipLibCheck, strict (+2 more)

### Community 16 - "manifest.json"
Cohesion: 0.50
Nodes (3): files, kit_version, purpose

### Community 36 - "ValidationError"
Cohesion: 0.33
Nodes (4): ensure_gateway_asset_kind(), GatewayViewSet, ValidationError, test_gateway_requires_gateway_kind()

### Community 37 - "AuthProvider.tsx"
Cohesion: 0.18
Nodes (12): ApiError, ApiErrorBody, authToken, get(), setAuthToken(), setUnauthorizedHandler(), Me, renderApp() (+4 more)

### Community 38 - "mqtt.py"
Cohesion: 0.18
Nodes (4): BaseAdapter, MqttAdapter, on_message(), _load_registry()

### Community 39 - "AppContext.tsx"
Cohesion: 0.24
Nodes (12): listTenants(), Tenant, AppContext, AppContextValue, AppProvider(), setProjectId(), setTenantId(), readStored() (+4 more)

### Community 52 - "apiFetch"
Cohesion: 0.15
Nodes (21): apiFetch(), createAsset(), createAssetType(), createAttribute(), deleteAsset(), deleteAssetType(), deleteAttribute(), health() (+13 more)

### Community 53 - "TenantScopedPermission"
Cohesion: 0.10
Nodes (7): apply_type_template(), AssetTypeViewSet, AssetViewSet, TenantScopedPermission, TenantScopedViewSet, AuditService, ProjectViewSet

### Community 54 - "AssetType"
Cohesion: 0.13
Nodes (15): Command, AssetType, Kind, seed_catalog_for_tenant(), validate_manifest(), test_all_manifests_validate(), test_gateway_manifests_have_connection_schema(), test_invalid_manifest_rejected() (+7 more)

### Community 55 - "telemetry/models.py"
Cohesion: 0.16
Nodes (11): AttributeCurrentAdmin, IngestMetricsAdmin, StoragePolicyAdmin, StoragePolicyStateAdmin, TelemetryPointAdmin, IngestMetrics, OwnerType, StoragePolicy (+3 more)

### Community 56 - "Requisitos normativos del producto (v2 — reestructurado por bounded context)"
Cohesion: 0.09
Nodes (22): Módulos, OAP-AIM — IA local y MCP, OAP-ASS — Asset Registry, OAP-BMS / OAP-EMS, OAP-CMM — Mantenimiento (paridad Atlas + mejoras OAP), OAP-CON — Conectividad (ADR-014; reemplaza OAP-MQT), OAP-DSH — Dashboards e Insights, OAP-ERP — Integración ERP (+14 more)

### Community 57 - "json"
Cohesion: 0.21
Nodes (3): _decode_payload(), collect(), main()

### Community 58 - "test_telemetry_policy.py"
Cohesion: 0.25
Nodes (14): subscribe_observer(), _history(), _ingest(), test_tel001_on_change_same_value_stores_once(), test_tel002_on_change_sequence(), test_tel003_boolean_transitions(), test_tel004_epsilon_absolute(), test_tel005_attribute_override_beats_agent_default() (+6 more)

### Community 59 - "Gateway"
Cohesion: 0.18
Nodes (11): Gateway, Meta, process_message(), topic_matches(), gateway_setup(), test_direct_ingest_on_change(), test_gateway_inline_creation(), test_gateway_inline_invalid_config_rolls_back() (+3 more)

### Community 60 - "Arquitectura maestra — OAP autonomous FOSS"
Cohesion: 0.12
Nodes (15): 10. Seguridad operacional, 11. Escalabilidad, 12. Deploy y actualización, 13. FOSS + documentación pública, 14. Criterios globales de aceptación, 1. Propósito, alcance y criterio de arquitectura, 2. Contexto C4 — actores y sistemas, 3. Contenedores lógicos (+7 more)

### Community 61 - "Plan de construcción secuencial para Kilo Code — NO crear todos los plugins de una vez"
Cohesion: 0.14
Nodes (13): Checklist común final, Plan de construcción secuencial para Kilo Code — NO crear todos los plugins de una vez, Principios, S00 — Antes de codificar, S01 — Bootstrap y vertical mínimo, S02 — Asset transaccional, S03 — Plugins y configuración, S04 — MQTT y política crítica (+5 more)

### Community 62 - "Backlog estructurado de funcionalidades — v3 (2026-11-17)"
Cohesion: 0.15
Nodes (12): Automatización (OAP-RUL), Backlog estructurado de funcionalidades — v3 (2026-11-17), BMS/EMS (OAP-BMS / OAP-EMS), Dashboards (OAP-DSH), Definition of priority, Frontend (OAP-UI) — rebuild total, Integraciones e IA (OAP-NRD / OAP-ERP / OAP-AIM), Mantenimiento (OAP-CMM) — paridad Atlas verificada (+4 more)

### Community 63 - "`cmms` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.15
Nodes (12): Autorización y configuración, `cmms` — Operaciones paso a paso, API, UX y fallas, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Solicitud PENDING -> APPROVED/REJECTED (auditable); aprobación crea orden idempotente., Flow 2: Orden NEW -> ASSIGNED -> IN_PROGRESS -> PAUSED -> COMPLETED -> CLOSED, con reopening autorizado y comentario obligatorio., Flow 3: Plan de mantenimiento calendario o medidor/condición genera como máximo 1 orden por ciclo definido. (+4 more)

### Community 64 - "`nodered` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.15
Nodes (12): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Import JSON/Admin API y parse nodes mqtt in/out/config, topics, JSONPath, transforms declarativas; detectar funciones JS no inferibles y marcar human-review., Flow 2: Proponer assets y point bindings con diff, identificación canonical, duplicados y escenario no reemplazar derechos/proyecto; commit tras aprobación., Flow 3: Exportar pestaña flow `tab` + nodes MQTT y opcionales transforms; placeholders secrets, metadatos OAP asset_id y hash, validar antes de POST /flow., Flow 4: Actualizar flow existente con concurrency check/hash; divergence manual ofrece merge/review en lugar de overwrite. (+4 more)

### Community 65 - "`ai_assistant` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): `ai_assistant` — Operaciones paso a paso, API, UX y fallas, Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Usuario consulta activos y fallas; RAG restringido por tenant+project sobre documentos y RDF; citar source ids sin inventar., Flow 2: Asistente genera propuesta SHACL/IEC/Node-RED/maintenance con preview diff, nunca modifica directo., Flow 3: Si solicita acción write, emite MCP/tool proposal, verifica RBAC y aprobación humana, graba audit. (+3 more)

### Community 66 - "Plugin `ai_assistant` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 67 - "Plugin `analytics` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 68 - "Plugin `bacnet` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 69 - "`bms` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, `bms` — Operaciones paso a paso, API, UX y fallas, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Crear building/floor/zones y equipos, vincular puntos Brick/Haystack y ubicación de planos., Flow 2: Widget HVAC muestra temp/mode/setpoint/alarms y permite propuesta de cambio validada., Flow 3: Planificador horario decide comandos con interlocks/roles y registro de ejecución. (+3 more)

### Community 70 - "Plugin `bms` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 71 - "Plugin `cmms` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 72 - "Plugin `dashboards` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 73 - "Plugin `edge` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 74 - "`ems` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, `ems` — Operaciones paso a paso, API, UX y fallas, Flow 1: Vincular medidor y atributos energía/potencia con unidades y time zone., Flow 2: Calcular demanda punta/fuera punta y consumo por período con calidad/no gaps silenciosos., Flow 3: Simular PV/BESS peak shaving separado de control real, con reserva SoC y límites. (+3 more)

### Community 75 - "Plugin `ems` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 76 - "Plugin `erp` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 77 - "`http_ws` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Configurar URL y método, comprobar allowlist DNS/IP/https y auth secret reference., Flow 2: Poll y parse JSONPath a atributos; respetar las mismas StoragePolicy que MQTT., Flow 3: Webhook firmado valida origen, timestamp, replay, proyecto y schema., Flow 4: WebSocket reconnect con backoff y carga acotada. (+3 more)

### Community 78 - "Plugin `http_ws` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 79 - "Plugin `inventory` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 80 - "`mcp_server` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Publicar tools lectura assets.search/get_graph, scenes.get, telemetry.query bounded y semantic.validate, limits., Flow 2: Exponer tools de escritura inicialmente solo `propose_*`; confirmar produce cambio mediante servicios DRF con auditoría., Flow 3: Aceptar sólo transporte recomendado por SDK vigente y validar tokens issuer/audience/scope TLS; no exponer creds LLM., Flow 4: Deshabilitar plugin inmediatamente bloquea nuevas invocaciones y mantiene auditoría. (+3 more)

### Community 81 - "Plugin `mcp_server` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 82 - "Plugin `modbus` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 83 - "`mqtt` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Admin registra broker TLS/ACL y agente con defaults on_change + N/1h; configura topic JSONPath y prueba preview sin escribir histórico., Flow 2: El broker entrega payload -> validate/schema/type/unit -> current+rules -> StoragePolicy -> PostgreSQL; el agente no delega sampling en Node-RED., Flow 3: Publish de command solamente mediante CommandService, topics allowlisted, TTL, retries y ACK si disponible., Flow 4: Autodiscovery crea propuesta de assets/attributes, no provisiona a tenant ni publica comandos sin confirmación. (+3 more)

### Community 84 - "Plugin `mqtt` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 85 - "Plugin `nodered` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 86 - "Plugin `protocol_extensions` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 87 - "ingest_event"
Cohesion: 0.12
Nodes (13): resolve_effective_policy(), _default_policy(), effective_policy(), ingest_event(), IngestResult, _lock_state(), _record_metrics(), _update_current() (+5 more)

### Community 88 - "CONTRATO NORMATIVO — Telemetría MQTT: persistir por cambio y máximo N valores/período"
Cohesion: 0.18
Nodes (10): 10. Anti-patrones bloqueantes, 1. Dos niveles de configuración, 2. Modelo de configuración propuesta, 3. Semántica de on_change, 4. Límite N muestras por ventana T, 5. Pipeline obligatorio (orden), 7. Replay, caída de conexión y consistencia, 8. API REST y UI (+2 more)

### Community 89 - "`analytics` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): `analytics` — Operaciones paso a paso, API, UX y fallas, Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Usuario define período, filtros y fuente autorizada; API optimiza agregaciones y ofrece CSV/JSON/PDF si plugin disponible., Flow 2: Históricos muestreados reportan policy de sampling, calidad, porcentaje discarded., Flow 3: CMMS cost/downtime MTTR/MTBF calculados con fixtures conocidos. (+2 more)

### Community 90 - "`bacnet` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, `bacnet` — Operaciones paso a paso, API, UX y fallas, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Descubrir dispositivo en red permitida (no escanear segmentos arbitrarios) y presentar assets/properties para aprobación., Flow 2: Leer propiedades con calidad e timestamps; COV con renewal y fallback poll controlado., Flow 3: Writes pasan CommandService y config de prioridad BACnet documentada y auditada. (+2 more)

### Community 91 - "`dashboards` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, `dashboards` — Operaciones paso a paso, API, UX y fallas, Definition of Done, Flow 1: Crear dashboard, arrastrar widget de historia/estado/mapa/alarma y bindear a atributo., Flow 2: Persistir layout versionado y revisar permisos de cada widget, incluso luego de disable addon., Flow 3: Stream realtime y series history consumen API autenticada, no acceso directo a DB. (+2 more)

### Community 92 - "`edge` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, `edge` — Operaciones paso a paso, API, UX y fallas, Flow 1: Provisionamiento bootstrap por token expirable un solo uso y binding al tenant., Flow 2: Gateway aplica conexiones/protocolos locales y almacena temporalmente al no tener red., Flow 3: Reconectar, replay bounded, dedupe, reconciliar cambios autorizados sin doble control. (+2 more)

### Community 93 - "`erp` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, `erp` — Operaciones paso a paso, API, UX y fallas, Flow 1: CMMS/Inventory solicita material -> outbox -> ERP adapter crea requisición con external reference., Flow 2: ERP aprueba/compra/recibe; webhook autenticado o poll actualiza estado replicado y enlaza a work order., Flow 3: Conflictos y retries usan idempotency/correlation ID; nunca factura/OC contable en OAP. (+2 more)

### Community 94 - "`inventory` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Stock inicial por depósito, entrada y transferencia con movimiento auditable., Flow 2: Orden reserva repuesto y al cerrar consume con transacción serializable o lock., Flow 3: Stock bajo mínimo produce solicitud de abastecimiento para ERP connector, no orden de compra local., `inventory` — Operaciones paso a paso, API, UX y fallas (+2 more)

### Community 95 - "`modbus` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Crear agent TCP o RTU, mapear registro holding/input/coil a Point del activo, declarar endian/escala/intervalo., Flow 2: Scheduler agrupa registros contiguos seguros, limita polling y convierte tipos, incluyendo signed/unsigned/float., Flow 3: Write pasa CommandService y validador de rangos; readback/ack cuando soportado., `modbus` — Operaciones paso a paso, API, UX y fallas (+2 more)

### Community 96 - "Escenarios específicos obligatorios"
Cohesion: 0.18
Nodes (10): Escenarios específicos obligatorios, Evidencia gate, `mqtt` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — 1000 payloads mismos valores -> 1 fila TSDB, 1000 current/rule observations y counters correctos., TEST-02 — Cambios 1,2,2,3 -> 3 filas si no aplica cap., TEST-03 — Agent N=2, Attribute N=5 -> 2 y 5 respectivamente en misma ventana, persistente al reinicio., TEST-04 — Dos workers compiten por cuota N=3 -> nunca 4 puntos. (+2 more)

### Community 97 - "`protocol_extensions` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Elegir driver de catálogo validado y configurar red/dispositivo, no ejecutar auto-discovery indiscriminado., Flow 2: Mapear datos a AssetAttribute con unidades/calidad, respetar StoragePolicy genérica y commands seguros., Flow 3: Proveer implementación nativa cuando sea viable o gateway de protocolo documentado sin hacer dependiente la app de Node-RED., `protocol_extensions` — Operaciones paso a paso, API, UX y fallas (+2 more)

### Community 98 - "django_apps"
Cohesion: 0.09
Nodes (8): AssetsConfig, seed_catalog_on_tenant_create(), ConnectivityConfig, CoreConfig, EventsConfig, PlatformConfig, PluginsConfig, TelemetryConfig

### Community 99 - "AssetAttribute"
Cohesion: 0.12
Nodes (10): AssetAttribute, Quality, ValueType, AssetAttributeViewSet, AttributeCurrent, Meta, TelemetryPoint, test_asset_crud_audit() (+2 more)

### Community 100 - "CORE / Api Realtime"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Api Realtime, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 101 - "CORE / Asset Registry"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Asset Registry, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 102 - "CORE / Attributes Commands"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Attributes Commands, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 103 - "CORE / Configuration Secrets"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Configuration Secrets, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 104 - "CORE / Dashboards Ui"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Dashboards Ui, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 105 - "CORE / Edge Provisioning"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Edge Provisioning, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 106 - "CORE / Events Outbox"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Events Outbox, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 107 - "CORE / Identity Authz"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Identity Authz, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 108 - "CORE / Notifications"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Notifications, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 109 - "CORE / Plugin Manager"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Plugin Manager, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 110 - "CORE / Projects Tenants"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Projects Tenants, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 111 - "CORE / Rules Alarms"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Rules Alarms, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 112 - "CORE / Semantics 81346 Brick Haystack"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Semantics 81346 Brick Haystack, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 113 - "CORE / Spatial Scenes"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Spatial Scenes, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 114 - "Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE"
Cohesion: 0.18
Nodes (10): Bloqueo del sandbox (no es déficit de código), Bloques de código entregados, C1 — Tipologías y plantillas (2026-11-17), C2 — Catálogo, Conectividad y UX de Activos (2026-11-18), Comandos exactos para reproducir, Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE, Fase 0 y Fase 1 — completadas (2026-11-17), Pendiente (plan aprobado) (+2 more)

### Community 115 - "Escenarios específicos obligatorios"
Cohesion: 0.20
Nodes (9): Escenarios específicos obligatorios, Evidencia gate, `nodered` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — JSON con 1 broker/2 sensors: preview correcto y commit idempotente., TEST-02 — Export JSON importable a pestaña Node-RED válida, sin credenciales., TEST-03 — Cambio manual de flow produce conflicto 409 y no sobrescribe., TEST-04 — Sin Node-RED la plataforma MQTT sigue funcionando al 100%. (+1 more)

### Community 116 - "mockServiceWorker.js"
Cohesion: 0.36
Nodes (8): activeClientIds, getResponse(), handleRequest(), IS_MOCKED_RESPONSE, resolveMainClient(), respondWithMock(), sendToClient(), serializeRequest()

### Community 117 - "platforms/admin.py"
Cohesion: 0.48
Nodes (5): AuditLogAdmin, MembershipAdmin, PlatformSettingAdmin, ProjectAdmin, TenantAdmin

### Community 118 - "OAP — Instrucciones vinculantes para cualquier agente de Kilo Code"
Cohesion: 0.22
Nodes (8): Calidad y no regresión, Lectura y ejecución inicial obligatoria, Límites estructurales, OAP — Instrucciones vinculantes para cualquier agente de Kilo Code, Requisitos, auditoría y UI, Rol y disciplina, Salida de cada tarea, Si faltan herramientas o dependencias

### Community 120 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `ai_assistant` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Prompt injection en documento no amplía scopes., TEST-02 — Usuario A no recupera embeddings/documentos de B., TEST-03 — LLM ausente no rompe API principal., TEST-04 — Aprobación requerida para escribir; acciones expiradas no ejecutan.

### Community 121 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `analytics` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Cálculo MTTR/MTBF sobre fixture manual coincide., TEST-02 — Export no filtra datos tenant externo., TEST-03 — Históricos sampling no producen falsas sumas de energía., TEST-04 — Cotas de tamaño/timeout evitan consultas costosas.

### Community 122 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `bacnet` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Simulador BACnet discover/read temperatura; offline y retry., TEST-02 — Subs COV expiry/re-subscribe sin duplicar., TEST-03 — Reject write a property read-only y sin permissions., TEST-04 — No discovery fuera de redes allowlisted.

### Community 123 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `bms` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Setpoint fuera rango y comando no autorizado se bloquea., TEST-02 — Control en zona A no modifica equipo de B., TEST-03 — Cambios horarios DST no duplican comandos., TEST-04 — Simulador equipo con error se refleja offline, alarma y CMMS trigger.

### Community 124 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `cmms` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Estado inválido o usuario sin rol devuelve 409/403 y no cambia., TEST-02 — Plan recurrente DST y 2 workers no crea orden duplicada., TEST-03 — Orden cerrada conserva logs/adjuntos/audit; permisos por proyecto., TEST-04 — Alarma repetida 100 veces genera 1 propuesta por incidencia.

### Community 125 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `dashboards` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Crear/editar/compartir dashboard E2E con reload., TEST-02 — Widget plugin deshabilitado queda placeholder sin perder configuración., TEST-03 — Sin permiso asset, widget no muestra datos sensibles., TEST-04 — Un lote 1000 sensores no causa miles requests no paginadas.

### Community 126 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `edge` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — 500 eventos offline reanudados sin duplicar; límite spool genera métrica., TEST-02 — Token enroll usado dos veces rechazado., TEST-03 — Gateway A no recibe credenciales/points de B., TEST-04 — Actualización de edge no destruye cursor/queue.

### Community 127 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `ems` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — kW vs kWh consistencia fixture y timezone tarifaria., TEST-02 — Agregación 15-min/mensual sin doble contar puntos repetidos., TEST-03 — Escenario no ejecuta comandos físicos., TEST-04 — Faltantes se reportan en vez de inventar consumo.

### Community 128 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `erp` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Dos reintentos de un pedido -> una requisición externa., TEST-02 — Callback con firma errónea o status ilegal no modifica estado., TEST-03 — ERP no disponible deja outbox pendiente e indicador., TEST-04 — CMMS puede seguir operando si conector ERP disabled.

### Community 129 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `http_ws` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — HTTP 5xx reintento acotado con DLQ., TEST-02 — SSRF contra localhost/metadata/reservadas bloqueado., TEST-03 — Webhook con firma inválida o replay rechazado., TEST-04 — Payload > máximo falla 413 y no se almacena.

### Community 130 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `inventory` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — Dos órdenes compitiendo stock no generan qty negativa., TEST-02 — Cancelar reserva restaura disponibilidad una sola vez., TEST-03 — Movimientos con unidad equivocada rechazados., TEST-04 — No se emite una OC local desde este plugin.

### Community 131 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `mcp_server` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — MCP client con token sin scopes obtiene forbidden., TEST-02 — Read tool nunca entrega assets tenant ajeno., TEST-03 — Tool write sin aprobación devuelve proposal id, no changes., TEST-04 — MCP disabled no expone herramientas y no rompe CORE.

### Community 132 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `modbus` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — Registro 40001 base1 vs addr0 verificado con simulador., TEST-02 — Poll 10 registros sin bloquear Django API., TEST-03 — Timeout/retry produce quality offline y no ocupa memoria sin límite., TEST-04 — Write denegado no llega al simulador.

### Community 133 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `protocol_extensions` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — Driver disabled no accede red., TEST-02 — Contrato de datos consistente entre MQTT/Modbus/BACnet/OPC UA., TEST-03 — Credenciales de protocolos aisladas y no visibles en export., TEST-04 — Pruebas simulador por protocolo, no stub.

### Community 134 - "Recorridos Playwright E2E de aplicación"
Cohesion: 0.22
Nodes (8): E2E-A: Primer login y proyecto, E2E-B: Plugin lifecycle, E2E-C: MQTT sampling, E2E-D: Mantenimiento, E2E-E: Escenas, E2E-F: Integraciones, Recorridos Playwright E2E de aplicación, UX checklist

### Community 136 - "Contrato de sandbox local, Docker y herramientas"
Cohesion: 0.25
Nodes (7): Acciones que requieren aprobación, Aislamiento de pruebas, Ambiente local obligatorio, Condición de bloqueo, Contrato de sandbox local, Docker y herramientas, Docker, Seguridad de agentes

### Community 137 - "ADR: Framework Django como core, no FastAPI"
Cohesion: 0.25
Nodes (7): ADR: Framework Django como core, no FastAPI, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 138 - "ADR: Producto independiente"
Cohesion: 0.25
Nodes (7): ADR: Producto independiente, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 139 - "ADR: Módulos estables y addons administrables"
Cohesion: 0.25
Nodes (7): ADR: Módulos estables y addons administrables, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 140 - "ADR: Single source of truth y propiedad"
Cohesion: 0.25
Nodes (7): ADR: Single source of truth y propiedad, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 141 - "ADR: Almacenamiento MQTT selectivo"
Cohesion: 0.25
Nodes (7): ADR: Almacenamiento MQTT selectivo, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 142 - "ADR: IEC/ISO 81346 + Brick + Haystack"
Cohesion: 0.25
Nodes (7): ADR: IEC/ISO 81346 + Brick + Haystack, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 143 - "ADR: SpatialScene multiproyecto"
Cohesion: 0.25
Nodes (7): ADR: SpatialScene multiproyecto, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 144 - "ADR: Seguridad de control físico"
Cohesion: 0.25
Nodes (7): ADR: Seguridad de control físico, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 145 - "ADR: Bootstrap automático PostgreSQL"
Cohesion: 0.25
Nodes (7): ADR: Bootstrap automático PostgreSQL, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 146 - "ADR: MCP y asistente local desacoplados"
Cohesion: 0.25
Nodes (7): ADR: MCP y asistente local desacoplados, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 147 - "ADR: ERP y Node-RED como externos"
Cohesion: 0.25
Nodes (7): ADR: ERP y Node-RED como externos, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 148 - "ADR: Licenciamiento verificable"
Cohesion: 0.25
Nodes (7): ADR: Licenciamiento verificable, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 149 - "Contrato de configuración ENV / DB / GUI"
Cohesion: 0.25
Nodes (7): Contrato de configuración ENV / DB / GUI, Ejemplo, Entidades de auditoría, Niveles y precedencia, Precedencia efectiva por clave, Resiliencia, Validación y UI

### Community 150 - "DB-B001 — Aprovisionamiento automático PostgreSQL/PostGIS"
Cohesion: 0.25
Nodes (7): 1. No confundir dos mecanismos, 2. Pipeline Compose y dependencias, 3. Algoritmo del job db-bootstrap, 4. Persistencia y recuperación, 5. Casos de prueba de aceptación DB-B001, 6. Referencias, DB-B001 — Aprovisionamiento automático PostgreSQL/PostGIS

### Community 151 - "Pruebas de contratos: REST, eventos, plugins, RDF, UI y MCP"
Cohesion: 0.25
Nodes (7): Eventos, MCP, Node-RED/ERP, Plugin, Pruebas de contratos: REST, eventos, plugins, RDF, UI y MCP, RDF/GIS, REST

### Community 152 - "Fixtures de QA sintéticas"
Cohesion: 0.25
Nodes (7): Activos/semántica, CMMS, Fixtures de QA sintéticas, MQTT, Node-RED, Proyectos, Seguridad

### Community 153 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @ant-design/icons, antd, echarts, i18next, react, react-dom, react-i18next (+2 more)

### Community 154 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, preview, test, test:e2e, typecheck

### Community 155 - "OAP — Open Asset Platform | Especificación integral para Kilo Code"
Cohesion: 0.25
Nodes (7): Licencias y atribución, Limitaciones de este kit, Navegación obligatoria, OAP — Open Asset Platform | Especificación integral para Kilo Code, Primer uso: NO comenzar creando 100 módulos vacíos, Requisitos críticos explícitos, Resultado buscado

### Community 156 - "TelemetryPage.tsx"
Cohesion: 0.38
Nodes (9): effectivePolicy(), gatewayStoragePolicy(), listGateways(), telemetryCurrent(), telemetryHistory(), telemetryStats(), HistoryChart(), PolicyModal() (+1 more)

### Community 157 - "telemetry/views.py"
Cohesion: 0.17
Nodes (6): IngestEventSerializer, HistoryService, StoragePolicyService, AttributeTelemetryViewSet, _get_attribute(), IngestView

### Community 158 - "endpoints.ts"
Cohesion: 0.15
Nodes (22): CreateAssetInput, CreateAssetTypeInput, CreateAttributeInput, listPlugins(), setPluginEnabled(), Asset, AssetAttribute, AssetType (+14 more)

### Community 159 - "OutboxEvent"
Cohesion: 0.13
Nodes (7): OutboxEventAdmin, Command, Meta, OutboxEvent, Status, dispatch_pending(), EventPublisher

### Community 160 - "Manual de orquestación Kilo Code: agentes, tareas y checkpoints"
Cohesion: 0.29
Nodes (6): Campos obligatorios del task brief, Manual de orquestación Kilo Code: agentes, tareas y checkpoints, Modelo de responsabilidad, Métricas de trabajo, Política de interrupción/reanudación, Protocolo de delegación

### Community 161 - "ADR: Almacenamiento de telemetría en tablas PostgreSQL regulares (sin TimescaleDB)"
Cohesion: 0.29
Nodes (6): ADR: Almacenamiento de telemetría en tablas PostgreSQL regulares (sin TimescaleDB), Alternativas consideradas, Consecuencias, Contexto, Decisión, Referencias internas

### Community 162 - "Diagramas de flujo C4 lógico + escenarios operativos"
Cohesion: 0.29
Nodes (6): Diagramas de flujo C4 lógico + escenarios operativos, Flujo cambio de plugin, Flujo DB primera ejecución, Flujo import/export Node-RED, Flujo MCP escritura, Flujo telemetría MQTT

### Community 163 - "Contrato de identidad, activos, IEC 81346 y RDF"
Cohesion: 0.29
Nodes (6): Contrato de identidad, activos, IEC 81346 y RDF, Identidades, Migración y consultas, Relación semántica, Tests, Versionado

### Community 164 - "Node-RED JSON bidireccional, modelo de negociación y export de pestaña"
Cohesion: 0.29
Nodes (6): Disparar procesos, Export, Import, Node-RED JSON bidireccional, modelo de negociación y export de pestaña, Preview → Commit, Pruebas

### Community 165 - "Contrato espacial — GIS/planos/escenas"
Cohesion: 0.29
Nodes (6): API models, Contrato espacial — GIS/planos/escenas, Edge cases, Endpoints, Flujo frontend, Validación

### Community 166 - "Esquema de telemetría y políticas de almacenamiento"
Cohesion: 0.29
Nodes (6): Consultas, Esquema de evento normalizado (`telemetry.observed.v1`), Esquema de telemetría y políticas de almacenamiento, Esquema StoragePolicy (`telemetry.storage-policy.v1`), Estados y métricas, Pruebas vinculantes

### Community 167 - "Docker Compose como distribución principal"
Cohesion: 0.29
Nodes (6): Build, Docker Compose como distribución principal, Roles de datos, Servicios y perfiles, Startup, Tests

### Community 168 - "Variables de entorno OAP — esquema, defaults, administración"
Cohesion: 0.29
Nodes (6): Archivo principal, Ejemplo importante, Grupos de configuración, Requisitos críticos telemetría, Variables de entorno OAP — esquema, defaults, administración, Variables y esquema validado

### Community 169 - "Rendimiento y observabilidad"
Cohesion: 0.29
Nodes (6): Alerta de saturación, BD, Carga reproducible, GIS/UI, Instrumentación, Rendimiento y observabilidad

### Community 170 - "Pruebas de seguridad negativas — por ruta/protocolo"
Cohesion: 0.29
Nodes (6): Authorization multitenancy, Commands/AI, Criterio de aprobación, DevSecOps, Pruebas de seguridad negativas — por ruta/protocolo, Web/app

### Community 171 - "Extracción de grafo de código de repositorios de referencia"
Cohesion: 0.29
Nodes (6): Extracción de grafo de código de repositorios de referencia, Fuente Atlas Java/Spring + React, Fuente OpenRemote Java/Gradle, Objetivos, Quality Gate, Resultados

### Community 172 - "Contexto persistente para Kilo Code: Open Asset Platform"
Cohesion: 0.33
Nodes (5): Contexto persistente para Kilo Code: Open Asset Platform, Decisiones cerradas, Interpretaciones de alcance, Leer antes de codificar, Objetivo innegociable

### Community 173 - "Modelo lógico SQL y owners"
Cohesion: 0.33
Nodes (5): Benchmarks, Esquemas recomendados, Integridad, Migraciones, Modelo lógico SQL y owners

### Community 174 - "REST, realtime y frontend plugin contract"
Cohesion: 0.33
Nodes (5): Convenciones, Frontend shell, Pruebas mínimas, REST, realtime y frontend plugin contract, Seguridad

### Community 175 - "Operación: backup, restauración y upgrades"
Cohesion: 0.33
Nodes (5): Backup y protección, DR y monitoreo, Operación: backup, restauración y upgrades, Restauración ensayada, Upgrade

### Community 176 - "GitHub CI, PR, releases y calidad de supply chain"
Cohesion: 0.33
Nodes (5): Checks de rendimiento, CI en cada PR, GitHub CI, PR, releases y calidad de supply chain, PR template, Release

### Community 177 - "Python .venv — instrucciones obligatorias para agentes"
Cohesion: 0.33
Nodes (5): Gestión dependencias, GitHub, Primer comando local, Python .venv — instrucciones obligatorias para agentes, Tests Django

### Community 178 - "`ai_assistant` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): `ai_assistant` — Esquema de datos, constraints y migraciones, Convenciones de persistencia, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 179 - "`analytics` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): `analytics` — Esquema de datos, constraints y migraciones, Convenciones de persistencia, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 180 - "`bacnet` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): `bacnet` — Esquema de datos, constraints y migraciones, Convenciones de persistencia, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 181 - "`bms` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): `bms` — Esquema de datos, constraints y migraciones, Convenciones de persistencia, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 182 - "`cmms` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): `cmms` — Esquema de datos, constraints y migraciones, Convenciones de persistencia, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 183 - "`dashboards` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, `dashboards` — Esquema de datos, constraints y migraciones, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 184 - "`edge` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, `edge` — Esquema de datos, constraints y migraciones, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 185 - "`ems` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, `ems` — Esquema de datos, constraints y migraciones, Entidades y campos de negocio, Transacciones críticas, Índices y pruebas migratorias

### Community 186 - "`erp` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `erp` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 187 - "`http_ws` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `http_ws` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 188 - "`inventory` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `inventory` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 189 - "`mcp_server` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `mcp_server` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 190 - "`modbus` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `modbus` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 191 - "`mqtt` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `mqtt` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 192 - "`nodered` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `nodered` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 193 - "`protocol_extensions` — Esquema de datos, constraints y migraciones"
Cohesion: 0.33
Nodes (5): Convenciones de persistencia, Entidades y campos de negocio, `protocol_extensions` — Esquema de datos, constraints y migraciones, Transacciones críticas, Índices y pruebas migratorias

### Community 194 - "Estrategia de verificación independiente"
Cohesion: 0.33
Nodes (5): Estrategia de verificación independiente, Pirámide de pruebas, Política fail-closed, Runbook CI, Verificación humana

### Community 195 - "Funcionalidad a partir de fuentes (auditoría ejecutada 2026-11-17)"
Cohesion: 0.33
Nodes (5): Atlas CMMS (`Grashjs/cmms`, commit `06abfe35`) — clasificación, Cómo auditar sin inventar (procedimiento), Funcionalidad a partir de fuentes (auditoría ejecutada 2026-11-17), Nuestro producto agrega (NEW_REQUIREMENT), OpenRemote Core (commit `6d46b473`) — clasificación

### Community 196 - "Integración ERP por requisición técnica"
Cohesion: 0.40
Nodes (4): Consistencia, Contrato outbound, Estado replicated inbound, Integración ERP por requisición técnica

### Community 197 - "Catálogo de eventos versionados"
Cohesion: 0.40
Nodes (4): Catálogo de eventos versionados, Envelope común, Eventos iniciales y owners, Evolución

### Community 198 - "Política de licencias FOSS, ingeniería limpia y publicación GitHub"
Cohesion: 0.40
Nodes (4): Auditoría obligatoria, Entregables previos a release, Gate, Política de licencias FOSS, ingeniería limpia y publicación GitHub

### Community 199 - "Plugin manifest — `ai_assistant`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `ai_assistant`, Versión, datos y garantías

### Community 200 - "Plugin manifest — `analytics`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `analytics`, Versión, datos y garantías

### Community 201 - "Plugin manifest — `bacnet`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `bacnet`, Versión, datos y garantías

### Community 202 - "Plugin manifest — `bms`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `bms`, Versión, datos y garantías

### Community 203 - "Plugin manifest — `cmms`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `cmms`, Versión, datos y garantías

### Community 204 - "Plugin manifest — `dashboards`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `dashboards`, Versión, datos y garantías

### Community 205 - "Plugin manifest — `edge`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `edge`, Versión, datos y garantías

### Community 206 - "Plugin manifest — `ems`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `ems`, Versión, datos y garantías

### Community 207 - "Plugin manifest — `erp`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `erp`, Versión, datos y garantías

### Community 208 - "Plugin manifest — `http_ws`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `http_ws`, Versión, datos y garantías

### Community 209 - "Plugin manifest — `inventory`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `inventory`, Versión, datos y garantías

### Community 210 - "Plugin manifest — `mcp_server`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `mcp_server`, Versión, datos y garantías

### Community 211 - "Plugin manifest — `modbus`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `modbus`, Versión, datos y garantías

### Community 212 - "Plugin manifest — `mqtt`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `mqtt`, Versión, datos y garantías

### Community 213 - "Plugin manifest — `nodered`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `nodered`, Versión, datos y garantías

### Community 214 - "Plugin manifest — `protocol_extensions`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `protocol_extensions`, Versión, datos y garantías

### Community 215 - "Definition of Done por historia y release"
Cohesion: 0.40
Nodes (4): Definition of Done por historia y release, Historia, Hito, Release

### Community 216 - "Índice de fuentes auditadas (2026-11-17)"
Cohesion: 0.40
Nodes (4): Clasificación aplicada en las matrices, Grashjs/cmms — Atlas CMMS (`06abfe35d09372ff80f889fcde73eb3cc71dc205`), openremote/core (`6d46b473d353533ccfc3938956eed145a134f2d8`), Índice de fuentes auditadas (2026-11-17)

### Community 217 - "Baselines de repositorios y estándares — fijar antes de implementar paridad"
Cohesion: 0.40
Nodes (4): Advertencia funcional, Baselines de repositorios y estándares — fijar antes de implementar paridad, Estándares y docs (sin cambio), Registro obligatorio

### Community 218 - "SYSTEM — Principal para agentes de construcción OAP"
Cohesion: 0.40
Nodes (4): Coordinación Kilo, Entrega por historia, SYSTEM — Principal para agentes de construcción OAP, Órdenes permanentes

### Community 220 - "Cómo interpretar “reconstruir todas las funcionalidades”"
Cohesion: 0.50
Nodes (3): Auditoría y cobertura, Cómo interpretar “reconstruir todas las funcionalidades”, No sustituir completitud por atajos

### Community 221 - "Registro de contratos OpenAPI (Fase 1)"
Cohesion: 0.50
Nodes (3): Estado por módulo, Procedimiento, Registro de contratos OpenAPI (Fase 1)

### Community 222 - "Aceptación del plugin `ai_assistant` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `ai_assistant` — G8, Evidencia requerida, Negativos obligatorios

### Community 223 - "Aceptación del plugin `analytics` — G9"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `analytics` — G9, Evidencia requerida, Negativos obligatorios

### Community 224 - "Aceptación del plugin `bacnet` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `bacnet` — G7, Evidencia requerida, Negativos obligatorios

### Community 225 - "Aceptación del plugin `bms` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `bms` — G7, Evidencia requerida, Negativos obligatorios

### Community 226 - "Aceptación del plugin `cmms` — G5"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `cmms` — G5, Evidencia requerida, Negativos obligatorios

### Community 227 - "Aceptación del plugin `dashboards` — G6"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `dashboards` — G6, Evidencia requerida, Negativos obligatorios

### Community 228 - "Aceptación del plugin `edge` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `edge` — G7, Evidencia requerida, Negativos obligatorios

### Community 229 - "Aceptación del plugin `ems` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `ems` — G7, Evidencia requerida, Negativos obligatorios

### Community 230 - "Aceptación del plugin `erp` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `erp` — G8, Evidencia requerida, Negativos obligatorios

### Community 231 - "Aceptación del plugin `http_ws` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `http_ws` — G7, Evidencia requerida, Negativos obligatorios

### Community 232 - "Aceptación del plugin `inventory` — G5"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `inventory` — G5, Evidencia requerida, Negativos obligatorios

### Community 233 - "Aceptación del plugin `mcp_server` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `mcp_server` — G8, Evidencia requerida, Negativos obligatorios

### Community 234 - "Aceptación del plugin `modbus` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `modbus` — G7, Evidencia requerida, Negativos obligatorios

### Community 235 - "Aceptación del plugin `mqtt` — G4"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `mqtt` — G4, Evidencia requerida, Negativos obligatorios

### Community 236 - "Aceptación del plugin `nodered` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `nodered` — G8, Evidencia requerida, Negativos obligatorios

### Community 237 - "Aceptación del plugin `protocol_extensions` — G9"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `protocol_extensions` — G9, Evidencia requerida, Negativos obligatorios

### Community 238 - "Puertas de calidad G0–G9 — fail-closed"
Cohesion: 0.50
Nodes (3): Bloqueos explícitos, Comandos mínimos propuestos una vez que exista código, Puertas de calidad G0–G9 — fail-closed

### Community 239 - "Casos deterministas para almacenar solo cambios y máximo N/T"
Cohesion: 0.50
Nodes (3): Casos deterministas para almacenar solo cambios y máximo N/T, Fixture generator, Load test

### Community 277 - "Patrones extraídos de repos de referencia (2026-11-17)"
Cohesion: 0.25
Nodes (7): 1. Navegación / menú, 2. Conectividad / gateways, 3. Dashboards y widgets de mapa, 4. Otros patrones relevantes, 5. Licencias (para auditoría OAP-FOSS), Patrones extraídos de repos de referencia (2026-11-17), Tabla tipo→fuente del catálogo semilla

### Community 278 - "ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes"
Cohesion: 0.33
Nodes (5): ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes, Alternativas consideradas, Consecuencias, Contexto, Decisión

### Community 279 - "connectivity/views.py"
Cohesion: 0.23
Nodes (5): GatewayBinding, GatewayBindingSerializer, GatewaySerializer, Meta, GatewayBindingViewSet

### Community 280 - "connectivity/services.py"
Cohesion: 0.28
Nodes (4): extract(), _gateway_connection_schema(), validate_gateway_config(), test_gateway_config_validation()

### Community 281 - "browser.ts"
Cohesion: 0.47
Nodes (4): enableMocks(), worker, handlers, msw

### Community 282 - "API MCP — permisos y aprobación"
Cohesion: 0.33
Nodes (5): API MCP — permisos y aprobación, Capas, Herramientas v1, Scopes, Tests

### Community 286 - "Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1)"
Cohesion: 0.25
Nodes (7): Bindings y dispositivos (ADR-014), Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1), i18n, Manifiesto (YAML/JSON), Reglas, Representación visual (ADR-016), Schemas de conexión predefinidos (patrones de OpenRemote/EdgeX/ThingsBoard)

### Community 290 - "ADR: Representación visual de activos e i18n estructural"
Cohesion: 0.33
Nodes (5): ADR: Representación visual de activos e i18n estructural, Alternativas consideradas, Consecuencias, Contexto, Decisión

### Community 294 - "index.ts"
Cohesion: 0.40
Nodes (4): Locale, resources, SUPPORTED_LOCALES, i18next

## Knowledge Gaps
- **1157 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Kind` (+1152 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1580 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **83 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `seed_catalog_on_tenant_create()` connect `django_apps` to `connectivity_worker.py`, `AssetType`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Gateway` (e.g. with `AssetViewSet` and `MqttAdapter`) actually correct?**
  _`Gateway` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Migration`, `Migration`, `Migration` to the rest of the system?**
  _1157 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `storage.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13846153846153847 - nodes in this community are weakly interconnected._
- **Why does `seed_catalog_for_tenant()` connect `AssetType` to `errors.py`, `django_apps`, `assets/views.py`, `connectivity_worker.py`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `AssetType` (e.g. with `AssetTypeSerializer` and `seed_catalog_for_tenant()`) actually correct?**
  _`AssetType` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `PluginManager` be split into smaller, more focused modules?**
  _Cohesion score 0.07377049180327869 - nodes in this community are weakly interconnected._