# Graph Report - Open-Asset-Platform  (2026-11-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2834 nodes · 4395 edges · 331 communities (229 shown, 102 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 338 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8d06768a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- django_db
- endpoints.ts
- apiFetch
- Asset
- errors.py
- dashboards/views.py
- django_apps
- Tenant
- App.tsx
- platforms/views.py
- AssetsPage.tsx
- AttributeTelemetryViewSet
- AdminPage.tsx
- connectivity/views.py
- ensure_db.py
- spatial/views.py
- AuthProvider.tsx
- conftest.py
- policy.py
- BaseAdapter
- Dashboard
- storage.py
- purge_project.py
- Requisitos normativos del producto (v2 — reestructurado por bounded context)
- PluginDefinition
- AssetType
- assets/views.py
- telemetry/views.py
- package.json
- devDependencies
- User
- GatewayBinding
- test_telemetry_policy.py
- compilerOptions
- UUIDPkModel
- core/views.py
- OutboxEvent
- MapsPage.tsx
- viewsets.py
- Gateway
- CanAdapter
- test_connectivity.py
- Arquitectura maestra — OAP autonomous FOSS
- .record
- Plan de construcción secuencial para Kilo Code — NO crear todos los plugins de una vez
- AssetViewSet
- django_contrib
- Backlog estructurado de funcionalidades — v3 (2026-11-17)
- `cmms` — Operaciones paso a paso, API, UX y fallas
- `nodered` — Operaciones paso a paso, API, UX y fallas
- assets/services.py
- Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE
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
- dependencies
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
- compilerOptions
- Contrato de extensibilidad OAP Plugin API v1
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
- Escenarios específicos obligatorios
- mockServiceWorker.js
- react-i18next
- OAP — Instrucciones vinculantes para cualquier agente de Kilo Code
- settings.py
- test_test_connection_waits_for_connack
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
- core/serializers.py
- Command
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
- Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1)
- Contrato de configuración ENV / DB / GUI
- DB-B001 — Aprovisionamiento automático PostgreSQL/PostGIS
- Pruebas de contratos: REST, eventos, plugins, RDF, UI y MCP
- Fixtures de QA sintéticas
- Patrones extraídos de repos de referencia (2026-11-17)
- scripts
- OAP — Open Asset Platform | Especificación integral para Kilo Code
- assets/admin.py
- ModbusAdapter
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
- Análisis de acercamiento a las normativas (81346 / Haystack / Brick / RDF-SHACL)
- seed_asset_types.py
- .run_forever
- connectivity_worker.py
- Command
- rest_framework_response
- ProjectMapConfigView
- Contexto persistente para Kilo Code: Open Asset Platform
- ADR: Navegación por bounded context y Conectividad como tipo de activo "Gateway"
- ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes
- ADR: Representación visual de activos e i18n estructural
- ADR: Jerarquía de activos, activos de ubicación y navegación arbórea
- ADR: Stack semántico (81346 + Brick/Haystack + RDF/SHACL)
- ADR: Dashboards tipo ThingsBoard + objeto Tendencia
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
- strip_control_chars
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
- vitest
- SYSTEM — Principal para agentes de construcción OAP
- connectivity/admin.py
- TenantScopedViewSet
- Command
- ConfigService
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
- manifest.json
- Grafo de dependencias planificado (NO grafo extraído del código fuente)
- Matriz trazabilidad de requisitos (v2 — esquema OAP-MOD-NNN)
- tsconfig.json
- architecture-auditor
- devops
- django-core
- frontend-ux
- iot-telemetry
- oap-lead
- plugin-integrations
- quality-security
- semantics-spatial
- G1.sh
- G2.sh
- G3.sh
- G4.sh
- quality_gate.sh
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
- @testing-library/jest-dom
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
- create_venv.sh
- gen_dev_secrets.sh
- oap-backend

## God Nodes (most connected - your core abstractions)
1. `apiFetch()` - 66 edges
2. `Gateway` - 63 edges
3. `Asset` - 45 edges
4. `AssetAttribute` - 41 edges
5. `GatewayBinding` - 40 edges
6. `AssetType` - 34 edges
7. `ingest_event()` - 34 edges
8. `Membership` - 33 edges
9. `Tenant` - 31 edges
10. `useAppContext()` - 28 edges

## Surprising Connections (you probably didn't know these)
- `Decisión` --references--> `Widget`  [INFERRED]
  docs/architecture/ADR-019-dashboards-trend.md → backend/dashboards/models.py
- `Integridad` --references--> `StoragePolicyState`  [INFERRED]
  docs/architecture/DB_LOGICAL_MODEL.md → backend/telemetry/models.py
- `Estados y métricas` --references--> `AttributeCurrent`  [INFERRED]
  docs/contracts/TELEMETRY_SCHEMA.md → backend/telemetry/models.py
- `C2 — Catálogo, Conectividad y UX de Activos (2026-11-18)` --references--> `apiFetch()`  [INFERRED]
  docs/evidence/IMPLEMENTATION_STATUS.md → frontend/src/api/client.ts
- `Decisión` --references--> `ingest_event()`  [INFERRED]
  docs/architecture/ADR-014-connectivity-gateway-navigation.md → backend/telemetry/storage.py

## Import Cycles
- None detected.

## Communities (331 total, 102 thin omitted)

### Community 0 - "django_db"
Cohesion: 0.06
Nodes (22): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+14 more)

### Community 1 - "endpoints.ts"
Cohesion: 0.08
Nodes (44): assetConnectivityStatus(), CreateAssetInput, CreateAssetTypeInput, CreateAttributeInput, createBinding(), createGateway(), Dashboard, DashboardBundle (+36 more)

### Community 2 - "apiFetch"
Cohesion: 0.13
Nodes (41): apiFetch(), applyTemplate(), createDashboard(), createWidget(), deleteWidget(), effectivePolicy(), exportBundle(), gatewayStoragePolicy() (+33 more)

### Community 3 - "Asset"
Cohesion: 0.09
Nodes (19): Asset, AssetAttribute, AssetRelationship, Meta, Quality, Status, ValueType, build_graph() (+11 more)

### Community 4 - "errors.py"
Cohesion: 0.09
Nodes (14): api_exception_handler(), ConflictError, DependencyUnavailableError, NotFoundError, OAPError, _problem(), _env_flag(), locked_slugs() (+6 more)

### Community 5 - "dashboards/views.py"
Cohesion: 0.11
Nodes (14): DashboardBundle, DashboardBundleSerializer, DashboardSerializer, DashboardTemplateSerializer, Meta, WidgetSerializer, _apply_definition(), DashboardBundleViewSet (+6 more)

### Community 6 - "django_apps"
Cohesion: 0.06
Nodes (10): AssetsConfig, seed_catalog_on_tenant_create(), ConnectivityConfig, CoreConfig, DashboardsConfig, EventsConfig, PlatformConfig, PluginsConfig (+2 more)

### Community 7 - "Tenant"
Cohesion: 0.07
Nodes (10): Command, Command, Tenant, test_asset_crud_audit(), test_asset_gateway_binding_on_create(), test_asset_type_template_creates_attributes(), test_delete_asset_purges_telemetry(), test_delete_tenant_purges_data() (+2 more)

### Community 8 - "App.tsx"
Cohesion: 0.13
Nodes (21): App(), IMPLEMENTED_PAGES, ProtectedLayout(), screenElement(), useAuth(), ErrorBoundary, Props, State (+13 more)

### Community 9 - "platforms/views.py"
Cohesion: 0.16
Nodes (15): AuditLog, Membership, AuditLogSerializer, MembershipSerializer, Meta, PlatformSettingSerializer, ProjectSerializer, TenantSerializer (+7 more)

### Community 10 - "AssetsPage.tsx"
Cohesion: 0.11
Nodes (24): createAsset(), createAssetType(), createAttribute(), deleteAsset(), deleteAssetType(), deleteAttribute(), listAssetTypes(), listUnits() (+16 more)

### Community 11 - "AttributeTelemetryViewSet"
Cohesion: 0.12
Nodes (10): _bucket_average(), HistoryService, _lttb(), StoragePolicyService, _with_gaps(), AttributeTelemetryViewSet, _get_attribute(), IngestView (+2 more)

### Community 12 - "AdminPage.tsx"
Cohesion: 0.15
Nodes (25): createProject(), createTenant(), deleteProject(), deleteTenant(), listProjects(), listTenants(), listUsers(), updateTenant() (+17 more)

### Community 13 - "connectivity/views.py"
Cohesion: 0.12
Nodes (11): GatewayBindingSerializer, GatewaySerializer, Meta, ensure_gateway_asset_kind(), _gateway_connection_schema(), validate_gateway_config(), GatewayBindingViewSet, GatewayViewSet (+3 more)

### Community 14 - "ensure_db.py"
Cohesion: 0.11
Nodes (12): _create_database(), _create_role(), _env(), _install_extensions(), main(), _read_secret(), _validate_identifier(), _wait_for_db() (+4 more)

### Community 15 - "spatial/views.py"
Cohesion: 0.15
Nodes (11): Meta, ProjectMapConfig, Scene, SceneLayer, ScenePlacement, Meta, SceneLayerSerializer, ScenePlacementSerializer (+3 more)

### Community 16 - "AuthProvider.tsx"
Cohesion: 0.11
Nodes (20): ApiError, ApiErrorBody, authToken, get(), setAuthToken(), setUnauthorizedHandler(), Me, renderApp() (+12 more)

### Community 17 - "conftest.py"
Cohesion: 0.13
Nodes (12): Role, request_context(), api(), asset(), attribute_factory(), _make(), _enable_db_for_all(), member_user() (+4 more)

### Community 18 - "policy.py"
Cohesion: 0.12
Nodes (8): canonical_json(), is_change(), merge_policy(), normalize_value(), utcnow(), window_bucket(), collect(), main()

### Community 20 - "Dashboard"
Cohesion: 0.13
Nodes (13): DashboardAdmin, WidgetAdmin, Dashboard, DashboardTemplate, Meta, Widget, WidgetType, TenantScopedModel (+5 more)

### Community 21 - "storage.py"
Cohesion: 0.15
Nodes (13): TelemetryPoint, parse_window(), _apply_policy(), _dedupe_key(), _default_policy(), effective_policy(), ingest_event(), IngestResult (+5 more)

### Community 22 - "purge_project.py"
Cohesion: 0.14
Nodes (12): AttributeCurrentAdmin, IngestMetricsAdmin, StoragePolicyAdmin, StoragePolicyStateAdmin, TelemetryPointAdmin, IngestMetrics, Meta, OwnerType (+4 more)

### Community 23 - "Requisitos normativos del producto (v2 — reestructurado por bounded context)"
Cohesion: 0.09
Nodes (22): Módulos, OAP-AIM — IA local y MCP, OAP-ASS — Asset Registry, OAP-BMS / OAP-EMS, OAP-CMM — Mantenimiento (paridad Atlas + mejoras OAP), OAP-CON — Conectividad (ADR-014; reemplaza OAP-MQT), OAP-DSH — Dashboards e Insights, OAP-ERP — Integración ERP (+14 more)

### Community 24 - "PluginDefinition"
Cohesion: 0.19
Nodes (16): PluginActivationAdmin, PluginDefinitionAdmin, PluginInstallationAdmin, PluginSettingsAdmin, Kind, Meta, PluginActivation, PluginDefinition (+8 more)

### Community 25 - "AssetType"
Cohesion: 0.20
Nodes (15): AssetType, Kind, seed_catalog_for_tenant(), validate_manifest(), test_all_manifests_validate(), test_gateway_manifests_have_connection_schema(), test_invalid_manifest_rejected(), test_location_types_seeded_with_semantics() (+7 more)

### Community 26 - "assets/views.py"
Cohesion: 0.17
Nodes (8): Unit, AssetAttributeSerializer, AssetSerializer, AssetTypeSerializer, Meta, UnitSerializer, AssetTypeViewSet, UnitViewSet

### Community 27 - "telemetry/views.py"
Cohesion: 0.16
Nodes (5): IsTenantMember, TenantScopedPermission, PluginSettingsViewSet, PluginViewSet, IngestEventSerializer

### Community 28 - "package.json"
Cohesion: 0.11
Nodes (19): name, private, type, version, echarts, eslint, @eslint/js, eslint-plugin-react-hooks (+11 more)

### Community 29 - "devDependencies"
Cohesion: 0.11
Nodes (19): devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom, msw (+11 more)

### Community 30 - "User"
Cohesion: 0.14
Nodes (4): RoleAdmin, UserAdmin, User, UserManager

### Community 31 - "GatewayBinding"
Cohesion: 0.21
Nodes (12): extract(), BindingType, GatewayBinding, _decode_payload(), infer_value_type(), _ingest(), ingest_device_payload(), process_message() (+4 more)

### Community 32 - "test_telemetry_policy.py"
Cohesion: 0.26
Nodes (14): AttributeCurrent, subscribe_observer(), _history(), _ingest(), test_tel001_on_change_same_value_stores_once(), test_tel002_on_change_sequence(), test_tel003_boolean_transitions(), test_tel004_epsilon_absolute() (+6 more)

### Community 33 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleDetection, moduleResolution (+9 more)

### Community 34 - "UUIDPkModel"
Cohesion: 0.18
Nodes (11): Meta, UUIDPkModel, AuditLogAdmin, MembershipAdmin, PlatformSettingAdmin, ProjectAdmin, TenantAdmin, Meta (+3 more)

### Community 35 - "core/views.py"
Cohesion: 0.17
Nodes (5): TokenObtainPairSerializer, HealthView, LoginView, MeView, RefreshView

### Community 36 - "OutboxEvent"
Cohesion: 0.16
Nodes (6): Command, Meta, OutboxEvent, Status, dispatch_pending(), EventPublisher

### Community 37 - "MapsPage.tsx"
Cohesion: 0.19
Nodes (14): addSceneLayer(), createPlacement(), createScene(), deletePlacement(), getMapConfig(), MapBounds, putMapConfig(), Scene (+6 more)

### Community 38 - "viewsets.py"
Cohesion: 0.17
Nodes (8): AuthzService, PermissionDeniedError, require_perm(), API MCP — permisos y aprobación, Capas, Herramientas v1, Scopes, Tests

### Community 39 - "Gateway"
Cohesion: 0.23
Nodes (8): BacnetAdapter, SnmpAdapter, Gateway, Meta, test_gateway_connection(), _test_mqtt(), test_test_connection_adapter_error_marks_status(), test_test_connection_delegates_to_adapter()

### Community 40 - "CanAdapter"
Cohesion: 0.20
Nodes (6): CanAdapter, MqttAdapter, OpcuaAdapter, poll(), _load_registry(), test_can_signal_decode()

### Community 41 - "test_connectivity.py"
Cohesion: 0.14
Nodes (10): asset_connectivity_status(), topic_matches(), gateway_setup(), test_asset_connectivity_status(), test_direct_ingest_on_change(), test_gateway_config_strips_control_chars(), test_gateway_inline_creation(), test_gateway_inline_invalid_config_rolls_back() (+2 more)

### Community 42 - "Arquitectura maestra — OAP autonomous FOSS"
Cohesion: 0.12
Nodes (15): 10. Seguridad operacional, 11. Escalabilidad, 12. Deploy y actualización, 13. FOSS + documentación pública, 14. Criterios globales de aceptación, 1. Propósito, alcance y criterio de arquitectura, 2. Contexto C4 — actores y sistemas, 3. Contenedores lógicos (+7 more)

### Community 44 - "Plan de construcción secuencial para Kilo Code — NO crear todos los plugins de una vez"
Cohesion: 0.14
Nodes (13): Checklist común final, Plan de construcción secuencial para Kilo Code — NO crear todos los plugins de una vez, Principios, S00 — Antes de codificar, S01 — Bootstrap y vertical mínimo, S02 — Asset transaccional, S03 — Plugins y configuración, S04 — MQTT y política crítica (+5 more)

### Community 46 - "django_contrib"
Cohesion: 0.18
Nodes (4): OutboxEventAdmin, SceneAdmin, SceneLayerAdmin, ScenePlacementAdmin

### Community 47 - "Backlog estructurado de funcionalidades — v3 (2026-11-17)"
Cohesion: 0.15
Nodes (12): Automatización (OAP-RUL), Backlog estructurado de funcionalidades — v3 (2026-11-17), BMS/EMS (OAP-BMS / OAP-EMS), Dashboards (OAP-DSH), Definition of priority, Frontend (OAP-UI) — rebuild total, Integraciones e IA (OAP-NRD / OAP-ERP / OAP-AIM), Mantenimiento (OAP-CMM) — paridad Atlas verificada (+4 more)

### Community 48 - "`cmms` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.15
Nodes (12): Autorización y configuración, `cmms` — Operaciones paso a paso, API, UX y fallas, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Solicitud PENDING -> APPROVED/REJECTED (auditable); aprobación crea orden idempotente., Flow 2: Orden NEW -> ASSIGNED -> IN_PROGRESS -> PAUSED -> COMPLETED -> CLOSED, con reopening autorizado y comentario obligatorio., Flow 3: Plan de mantenimiento calendario o medidor/condición genera como máximo 1 orden por ciclo definido. (+4 more)

### Community 49 - "`nodered` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.15
Nodes (12): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Import JSON/Admin API y parse nodes mqtt in/out/config, topics, JSONPath, transforms declarativas; detectar funciones JS no inferibles y marcar human-review., Flow 2: Proponer assets y point bindings con diff, identificación canonical, duplicados y escenario no reemplazar derechos/proyecto; commit tras aprobación., Flow 3: Exportar pestaña flow `tab` + nodes MQTT y opcionales transforms; placeholders secrets, metadatos OAP asset_id y hash, validar antes de POST /flow., Flow 4: Actualizar flow existente con concurrency check/hash; divergence manual ofrece merge/review en lugar de overwrite. (+4 more)

### Community 50 - "assets/services.py"
Cohesion: 0.18
Nodes (6): apply_type_template(), AssetService, AttributeService, set_designation(), suggest_designation_occurrence(), test_set_designation_versions_and_auto_occurrence()

### Community 51 - "Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE"
Cohesion: 0.17
Nodes (11): Bloqueo del sandbox (no es déficit de código), Bloques de código entregados, C1 — Tipologías y plantillas (2026-11-17), C2 — Catálogo, Conectividad y UX de Activos (2026-11-18), C3 — Idioma/timezone, usuarios, proyectos, MapConfig (2026-11-18), Comandos exactos para reproducir, Estado de implementación — ACTUALIZAR DESPUÉS DE CADA GATE, Fase 0 y Fase 1 — completadas (2026-11-17) (+3 more)

### Community 52 - "`ai_assistant` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): `ai_assistant` — Operaciones paso a paso, API, UX y fallas, Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Usuario consulta activos y fallas; RAG restringido por tenant+project sobre documentos y RDF; citar source ids sin inventar., Flow 2: Asistente genera propuesta SHACL/IEC/Node-RED/maintenance con preview diff, nunca modifica directo., Flow 3: Si solicita acción write, emite MCP/tool proposal, verifica RBAC y aprobación humana, graba audit. (+3 more)

### Community 53 - "Plugin `ai_assistant` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 54 - "Plugin `analytics` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 55 - "Plugin `bacnet` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 56 - "`bms` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, `bms` — Operaciones paso a paso, API, UX y fallas, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Crear building/floor/zones y equipos, vincular puntos Brick/Haystack y ubicación de planos., Flow 2: Widget HVAC muestra temp/mode/setpoint/alarms y permite propuesta de cambio validada., Flow 3: Planificador horario decide comandos con interlocks/roles y registro de ejecución. (+3 more)

### Community 57 - "Plugin `bms` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 58 - "Plugin `cmms` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 59 - "Plugin `dashboards` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 60 - "Plugin `edge` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 61 - "`ems` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, `ems` — Operaciones paso a paso, API, UX y fallas, Flow 1: Vincular medidor y atributos energía/potencia con unidades y time zone., Flow 2: Calcular demanda punta/fuera punta y consumo por período con calidad/no gaps silenciosos., Flow 3: Simular PV/BESS peak shaving separado de control real, con reserva SoC y límites. (+3 more)

### Community 62 - "Plugin `ems` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 63 - "Plugin `erp` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 64 - "`http_ws` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Configurar URL y método, comprobar allowlist DNS/IP/https y auth secret reference., Flow 2: Poll y parse JSONPath a atributos; respetar las mismas StoragePolicy que MQTT., Flow 3: Webhook firmado valida origen, timestamp, replay, proyecto y schema., Flow 4: WebSocket reconnect con backoff y carga acotada. (+3 more)

### Community 65 - "Plugin `http_ws` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 66 - "Plugin `inventory` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 67 - "`mcp_server` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Publicar tools lectura assets.search/get_graph, scenes.get, telemetry.query bounded y semantic.validate, limits., Flow 2: Exponer tools de escritura inicialmente solo `propose_*`; confirmar produce cambio mediante servicios DRF con auditoría., Flow 3: Aceptar sólo transporte recomendado por SDK vigente y validar tokens issuer/audience/scope TLS; no exponer creds LLM., Flow 4: Deshabilitar plugin inmediatamente bloquea nuevas invocaciones y mantiene auditoría. (+3 more)

### Community 68 - "Plugin `mcp_server` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 69 - "Plugin `modbus` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 70 - "`mqtt` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.17
Nodes (11): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Admin registra broker TLS/ACL y agente con defaults on_change + N/1h; configura topic JSONPath y prueba preview sin escribir histórico., Flow 2: El broker entrega payload -> validate/schema/type/unit -> current+rules -> StoragePolicy -> PostgreSQL; el agente no delega sampling en Node-RED., Flow 3: Publish de command solamente mediante CommandService, topics allowlisted, TTL, retries y ACK si disponible., Flow 4: Autodiscovery crea propuesta de assets/attributes, no provisiona a tenant ni publica comandos sin confirmación. (+3 more)

### Community 71 - "Plugin `mqtt` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 72 - "Plugin `nodered` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 73 - "Plugin `protocol_extensions` — especificación funcional y técnica"
Cohesion: 0.17
Nodes (11): Configuración ambiental (solo defaults y parámetros de despliegue), Dependencias (contratos públicos; no imports privados), Documentos vinculados, Eventos, permisos y estado, Historias de usuario y workflows de extremo a extremo, Interfaz HTTP — endpoints a especificar en OpenAPI v1, Interfaz React / criterios UX, Modelo propio de dominio / tablas (borrador a formalizar migrando) (+3 more)

### Community 74 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @ant-design/icons, antd, echarts, i18next, maplibre-gl, react, react-dom (+4 more)

### Community 75 - "CONTRATO NORMATIVO — Telemetría MQTT: persistir por cambio y máximo N valores/período"
Cohesion: 0.18
Nodes (10): 10. Anti-patrones bloqueantes, 1. Dos niveles de configuración, 2. Modelo de configuración propuesta, 3. Semántica de on_change, 4. Límite N muestras por ventana T, 5. Pipeline obligatorio (orden), 7. Replay, caída de conexión y consistencia, 8. API REST y UI (+2 more)

### Community 76 - "`analytics` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): `analytics` — Operaciones paso a paso, API, UX y fallas, Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Usuario define período, filtros y fuente autorizada; API optimiza agregaciones y ofrece CSV/JSON/PDF si plugin disponible., Flow 2: Históricos muestreados reportan policy de sampling, calidad, porcentaje discarded., Flow 3: CMMS cost/downtime MTTR/MTBF calculados con fixtures conocidos. (+2 more)

### Community 77 - "`bacnet` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, `bacnet` — Operaciones paso a paso, API, UX y fallas, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Descubrir dispositivo en red permitida (no escanear segmentos arbitrarios) y presentar assets/properties para aprobación., Flow 2: Leer propiedades con calidad e timestamps; COV con renewal y fallback poll controlado., Flow 3: Writes pasan CommandService y config de prioridad BACnet documentada y auditada. (+2 more)

### Community 78 - "`dashboards` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, `dashboards` — Operaciones paso a paso, API, UX y fallas, Definition of Done, Flow 1: Crear dashboard, arrastrar widget de historia/estado/mapa/alarma y bindear a atributo., Flow 2: Persistir layout versionado y revisar permisos de cada widget, incluso luego de disable addon., Flow 3: Stream realtime y series history consumen API autenticada, no acceso directo a DB. (+2 more)

### Community 79 - "`edge` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, `edge` — Operaciones paso a paso, API, UX y fallas, Flow 1: Provisionamiento bootstrap por token expirable un solo uso y binding al tenant., Flow 2: Gateway aplica conexiones/protocolos locales y almacena temporalmente al no tener red., Flow 3: Reconectar, replay bounded, dedupe, reconciliar cambios autorizados sin doble control. (+2 more)

### Community 80 - "`erp` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, `erp` — Operaciones paso a paso, API, UX y fallas, Flow 1: CMMS/Inventory solicita material -> outbox -> ERP adapter crea requisición con external reference., Flow 2: ERP aprueba/compra/recibe; webhook autenticado o poll actualiza estado replicado y enlaza a work order., Flow 3: Conflictos y retries usan idempotency/correlation ID; nunca factura/OC contable en OAP. (+2 more)

### Community 81 - "`inventory` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Stock inicial por depósito, entrada y transferencia con movimiento auditable., Flow 2: Orden reserva repuesto y al cerrar consume con transacción serializable o lock., Flow 3: Stock bajo mínimo produce solicitud de abastecimiento para ERP connector, no orden de compra local., `inventory` — Operaciones paso a paso, API, UX y fallas (+2 more)

### Community 82 - "`modbus` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Crear agent TCP o RTU, mapear registro holding/input/coil a Point del activo, declarar endian/escala/intervalo., Flow 2: Scheduler agrupa registros contiguos seguros, limita polling y convierte tipos, incluyendo signed/unsigned/float., Flow 3: Write pasa CommandService y validador de rangos; readback/ack cuando soportado., `modbus` — Operaciones paso a paso, API, UX y fallas (+2 more)

### Community 83 - "Escenarios específicos obligatorios"
Cohesion: 0.18
Nodes (10): Escenarios específicos obligatorios, Evidencia gate, `mqtt` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — 1000 payloads mismos valores -> 1 fila TSDB, 1000 current/rule observations y counters correctos., TEST-02 — Cambios 1,2,2,3 -> 3 filas si no aplica cap., TEST-03 — Agent N=2, Attribute N=5 -> 2 y 5 respectivamente en misma ventana, persistente al reinicio., TEST-04 — Dos workers compiten por cuota N=3 -> nunca 4 puntos. (+2 more)

### Community 84 - "`protocol_extensions` — Operaciones paso a paso, API, UX y fallas"
Cohesion: 0.18
Nodes (10): Autorización y configuración, Compatibilidad, error handling y health, Contrato HTTP a implementar y documentar, Definition of Done, Flow 1: Elegir driver de catálogo validado y configurar red/dispositivo, no ejecutar auto-discovery indiscriminado., Flow 2: Mapear datos a AssetAttribute con unidades/calidad, respetar StoragePolicy genérica y commands seguros., Flow 3: Proveer implementación nativa cuando sea viable o gateway de protocolo documentado sin hacer dependiente la app de Node-RED., `protocol_extensions` — Operaciones paso a paso, API, UX y fallas (+2 more)

### Community 85 - "compilerOptions"
Cohesion: 0.18
Nodes (10): compilerOptions, allowSyntheticDefaultImports, lib, module, moduleResolution, noEmit, skipLibCheck, strict (+2 more)

### Community 86 - "Contrato de extensibilidad OAP Plugin API v1"
Cohesion: 0.20
Nodes (9): RequestContext, 1. Objetivo y restricción Django, 2. Manifiesto (semántica a implementarse), 3. APIs core para plugins, 5. API REST propuesta, 6. UI ExtensionManifest, 7. Actualización y compatibilidad, 8. Tests obligatorios (+1 more)

### Community 87 - "CORE / Api Realtime"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Api Realtime, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 88 - "CORE / Asset Registry"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Asset Registry, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 89 - "CORE / Attributes Commands"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Attributes Commands, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 90 - "CORE / Configuration Secrets"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Configuration Secrets, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 91 - "CORE / Dashboards Ui"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Dashboards Ui, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 92 - "CORE / Edge Provisioning"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Edge Provisioning, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 93 - "CORE / Events Outbox"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Events Outbox, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 94 - "CORE / Identity Authz"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Identity Authz, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 95 - "CORE / Notifications"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Notifications, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 96 - "CORE / Plugin Manager"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Plugin Manager, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 97 - "CORE / Projects Tenants"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Projects Tenants, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 98 - "CORE / Rules Alarms"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Rules Alarms, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 99 - "CORE / Semantics 81346 Brick Haystack"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Semantics 81346 Brick Haystack, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 100 - "CORE / Spatial Scenes"
Cohesion: 0.20
Nodes (9): Casos negativos comunes, CORE / Spatial Scenes, Dependencias y compatibilidad, Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes, Entidades y campos propuestos (Django models; ajustar con ADR si cambia), Flujo de implementación mínimo, Invariantes funcionales / reglas de negocio, Objetivo de producto y límites de propiedad (+1 more)

### Community 101 - "Escenarios específicos obligatorios"
Cohesion: 0.20
Nodes (9): Escenarios específicos obligatorios, Evidencia gate, `nodered` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — JSON con 1 broker/2 sensors: preview correcto y commit idempotente., TEST-02 — Export JSON importable a pestaña Node-RED válida, sin credenciales., TEST-03 — Cambio manual de flow produce conflicto 409 y no sobrescribe., TEST-04 — Sin Node-RED la plataforma MQTT sigue funcionando al 100%. (+1 more)

### Community 102 - "mockServiceWorker.js"
Cohesion: 0.36
Nodes (8): activeClientIds, getResponse(), handleRequest(), IS_MOCKED_RESPONSE, resolveMainClient(), respondWithMock(), sendToClient(), serializeRequest()

### Community 103 - "react-i18next"
Cohesion: 0.22
Nodes (8): OapRuntimeConfig, RUNTIME, Window, Locale, resources, SUPPORTED_LOCALES, i18next, react-i18next

### Community 104 - "OAP — Instrucciones vinculantes para cualquier agente de Kilo Code"
Cohesion: 0.22
Nodes (8): Calidad y no regresión, Lectura y ejecución inicial obligatoria, Límites estructurales, OAP — Instrucciones vinculantes para cualquier agente de Kilo Code, Requisitos, auditoría y UI, Rol y disciplina, Salida de cada tarea, Si faltan herramientas o dependencias

### Community 107 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `ai_assistant` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Prompt injection en documento no amplía scopes., TEST-02 — Usuario A no recupera embeddings/documentos de B., TEST-03 — LLM ausente no rompe API principal., TEST-04 — Aprobación requerida para escribir; acciones expiradas no ejecutan.

### Community 108 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `analytics` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Cálculo MTTR/MTBF sobre fixture manual coincide., TEST-02 — Export no filtra datos tenant externo., TEST-03 — Históricos sampling no producen falsas sumas de energía., TEST-04 — Cotas de tamaño/timeout evitan consultas costosas.

### Community 109 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `bacnet` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Simulador BACnet discover/read temperatura; offline y retry., TEST-02 — Subs COV expiry/re-subscribe sin duplicar., TEST-03 — Reject write a property read-only y sin permissions., TEST-04 — No discovery fuera de redes allowlisted.

### Community 110 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `bms` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Setpoint fuera rango y comando no autorizado se bloquea., TEST-02 — Control en zona A no modifica equipo de B., TEST-03 — Cambios horarios DST no duplican comandos., TEST-04 — Simulador equipo con error se refleja offline, alarma y CMMS trigger.

### Community 111 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `cmms` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Estado inválido o usuario sin rol devuelve 409/403 y no cambia., TEST-02 — Plan recurrente DST y 2 workers no crea orden duplicada., TEST-03 — Orden cerrada conserva logs/adjuntos/audit; permisos por proyecto., TEST-04 — Alarma repetida 100 veces genera 1 propuesta por incidencia.

### Community 112 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `dashboards` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Crear/editar/compartir dashboard E2E con reload., TEST-02 — Widget plugin deshabilitado queda placeholder sin perder configuración., TEST-03 — Sin permiso asset, widget no muestra datos sensibles., TEST-04 — Un lote 1000 sensores no causa miles requests no paginadas.

### Community 113 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `edge` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — 500 eventos offline reanudados sin duplicar; límite spool genera métrica., TEST-02 — Token enroll usado dos veces rechazado., TEST-03 — Gateway A no recibe credenciales/points de B., TEST-04 — Actualización de edge no destruye cursor/queue.

### Community 114 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `ems` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — kW vs kWh consistencia fixture y timezone tarifaria., TEST-02 — Agregación 15-min/mensual sin doble contar puntos repetidos., TEST-03 — Escenario no ejecuta comandos físicos., TEST-04 — Faltantes se reportan en vez de inventar consumo.

### Community 115 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): `erp` — Escenarios Given/When/Then y evidencias, Escenarios específicos obligatorios, Evidencia gate, Suite común no negociable, TEST-01 — Dos reintentos de un pedido -> una requisición externa., TEST-02 — Callback con firma errónea o status ilegal no modifica estado., TEST-03 — ERP no disponible deja outbox pendiente e indicador., TEST-04 — CMMS puede seguir operando si conector ERP disabled.

### Community 116 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `http_ws` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — HTTP 5xx reintento acotado con DLQ., TEST-02 — SSRF contra localhost/metadata/reservadas bloqueado., TEST-03 — Webhook con firma inválida o replay rechazado., TEST-04 — Payload > máximo falla 413 y no se almacena.

### Community 117 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `inventory` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — Dos órdenes compitiendo stock no generan qty negativa., TEST-02 — Cancelar reserva restaura disponibilidad una sola vez., TEST-03 — Movimientos con unidad equivocada rechazados., TEST-04 — No se emite una OC local desde este plugin.

### Community 118 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `mcp_server` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — MCP client con token sin scopes obtiene forbidden., TEST-02 — Read tool nunca entrega assets tenant ajeno., TEST-03 — Tool write sin aprobación devuelve proposal id, no changes., TEST-04 — MCP disabled no expone herramientas y no rompe CORE.

### Community 119 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `modbus` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — Registro 40001 base1 vs addr0 verificado con simulador., TEST-02 — Poll 10 registros sin bloquear Django API., TEST-03 — Timeout/retry produce quality offline y no ocupa memoria sin límite., TEST-04 — Write denegado no llega al simulador.

### Community 120 - "Escenarios específicos obligatorios"
Cohesion: 0.22
Nodes (8): Escenarios específicos obligatorios, Evidencia gate, `protocol_extensions` — Escenarios Given/When/Then y evidencias, Suite común no negociable, TEST-01 — Driver disabled no accede red., TEST-02 — Contrato de datos consistente entre MQTT/Modbus/BACnet/OPC UA., TEST-03 — Credenciales de protocolos aisladas y no visibles en export., TEST-04 — Pruebas simulador por protocolo, no stub.

### Community 121 - "Recorridos Playwright E2E de aplicación"
Cohesion: 0.22
Nodes (8): E2E-A: Primer login y proyecto, E2E-B: Plugin lifecycle, E2E-C: MQTT sampling, E2E-D: Mantenimiento, E2E-E: Escenas, E2E-F: Integraciones, Recorridos Playwright E2E de aplicación, UX checklist

### Community 122 - "core/serializers.py"
Cohesion: 0.29
Nodes (3): Meta, UserCreateSerializer, UserSerializer

### Community 124 - "Contrato de sandbox local, Docker y herramientas"
Cohesion: 0.25
Nodes (7): Acciones que requieren aprobación, Aislamiento de pruebas, Ambiente local obligatorio, Condición de bloqueo, Contrato de sandbox local, Docker y herramientas, Docker, Seguridad de agentes

### Community 125 - "ADR: Framework Django como core, no FastAPI"
Cohesion: 0.25
Nodes (7): ADR: Framework Django como core, no FastAPI, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 126 - "ADR: Producto independiente"
Cohesion: 0.25
Nodes (7): ADR: Producto independiente, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 127 - "ADR: Módulos estables y addons administrables"
Cohesion: 0.25
Nodes (7): ADR: Módulos estables y addons administrables, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 128 - "ADR: Single source of truth y propiedad"
Cohesion: 0.25
Nodes (7): ADR: Single source of truth y propiedad, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 129 - "ADR: Almacenamiento MQTT selectivo"
Cohesion: 0.25
Nodes (7): ADR: Almacenamiento MQTT selectivo, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 130 - "ADR: IEC/ISO 81346 + Brick + Haystack"
Cohesion: 0.25
Nodes (7): ADR: IEC/ISO 81346 + Brick + Haystack, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 131 - "ADR: SpatialScene multiproyecto"
Cohesion: 0.25
Nodes (7): ADR: SpatialScene multiproyecto, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 132 - "ADR: Seguridad de control físico"
Cohesion: 0.25
Nodes (7): ADR: Seguridad de control físico, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 133 - "ADR: Bootstrap automático PostgreSQL"
Cohesion: 0.25
Nodes (7): ADR: Bootstrap automático PostgreSQL, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 134 - "ADR: MCP y asistente local desacoplados"
Cohesion: 0.25
Nodes (7): ADR: MCP y asistente local desacoplados, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 135 - "ADR: ERP y Node-RED como externos"
Cohesion: 0.25
Nodes (7): ADR: ERP y Node-RED como externos, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 136 - "ADR: Licenciamiento verificable"
Cohesion: 0.25
Nodes (7): ADR: Licenciamiento verificable, Alternativas consideradas, Consecuencias, Contexto, Decisión, Pruebas de decisión, Referencias internas

### Community 137 - "Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1)"
Cohesion: 0.25
Nodes (7): Bindings y dispositivos (ADR-014), Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1), i18n, Manifiesto (YAML/JSON), Reglas, Representación visual (ADR-016), Schemas de conexión predefinidos (patrones de OpenRemote/EdgeX/ThingsBoard)

### Community 138 - "Contrato de configuración ENV / DB / GUI"
Cohesion: 0.25
Nodes (7): Contrato de configuración ENV / DB / GUI, Ejemplo, Entidades de auditoría, Niveles y precedencia, Precedencia efectiva por clave, Resiliencia, Validación y UI

### Community 139 - "DB-B001 — Aprovisionamiento automático PostgreSQL/PostGIS"
Cohesion: 0.25
Nodes (7): 1. No confundir dos mecanismos, 2. Pipeline Compose y dependencias, 3. Algoritmo del job db-bootstrap, 4. Persistencia y recuperación, 5. Casos de prueba de aceptación DB-B001, 6. Referencias, DB-B001 — Aprovisionamiento automático PostgreSQL/PostGIS

### Community 140 - "Pruebas de contratos: REST, eventos, plugins, RDF, UI y MCP"
Cohesion: 0.25
Nodes (7): Eventos, MCP, Node-RED/ERP, Plugin, Pruebas de contratos: REST, eventos, plugins, RDF, UI y MCP, RDF/GIS, REST

### Community 141 - "Fixtures de QA sintéticas"
Cohesion: 0.25
Nodes (7): Activos/semántica, CMMS, Fixtures de QA sintéticas, MQTT, Node-RED, Proyectos, Seguridad

### Community 142 - "Patrones extraídos de repos de referencia (2026-11-17)"
Cohesion: 0.25
Nodes (7): 1. Navegación / menú, 2. Conectividad / gateways, 3. Dashboards y widgets de mapa, 4. Otros patrones relevantes, 5. Licencias (para auditoría OAP-FOSS), Patrones extraídos de repos de referencia (2026-11-17), Tabla tipo→fuente del catálogo semilla

### Community 143 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, preview, test, test:e2e, typecheck

### Community 144 - "OAP — Open Asset Platform | Especificación integral para Kilo Code"
Cohesion: 0.25
Nodes (7): Licencias y atribución, Limitaciones de este kit, Navegación obligatoria, OAP — Open Asset Platform | Especificación integral para Kilo Code, Primer uso: NO comenzar creando 100 módulos vacíos, Requisitos críticos explícitos, Resultado buscado

### Community 145 - "assets/admin.py"
Cohesion: 0.48
Nodes (5): AssetAdmin, AssetAttributeAdmin, AssetRelationshipAdmin, AssetTypeAdmin, UnitAdmin

### Community 147 - "Manual de orquestación Kilo Code: agentes, tareas y checkpoints"
Cohesion: 0.29
Nodes (6): Campos obligatorios del task brief, Manual de orquestación Kilo Code: agentes, tareas y checkpoints, Modelo de responsabilidad, Métricas de trabajo, Política de interrupción/reanudación, Protocolo de delegación

### Community 148 - "ADR: Almacenamiento de telemetría en tablas PostgreSQL regulares (sin TimescaleDB)"
Cohesion: 0.29
Nodes (6): ADR: Almacenamiento de telemetría en tablas PostgreSQL regulares (sin TimescaleDB), Alternativas consideradas, Consecuencias, Contexto, Decisión, Referencias internas

### Community 149 - "Diagramas de flujo C4 lógico + escenarios operativos"
Cohesion: 0.29
Nodes (6): Diagramas de flujo C4 lógico + escenarios operativos, Flujo cambio de plugin, Flujo DB primera ejecución, Flujo import/export Node-RED, Flujo MCP escritura, Flujo telemetría MQTT

### Community 150 - "Contrato de identidad, activos, IEC 81346 y RDF"
Cohesion: 0.29
Nodes (6): Contrato de identidad, activos, IEC 81346 y RDF, Identidades, Migración y consultas, Relación semántica, Tests, Versionado

### Community 151 - "Node-RED JSON bidireccional, modelo de negociación y export de pestaña"
Cohesion: 0.29
Nodes (6): Disparar procesos, Export, Import, Node-RED JSON bidireccional, modelo de negociación y export de pestaña, Preview → Commit, Pruebas

### Community 152 - "Contrato espacial — GIS/planos/escenas"
Cohesion: 0.29
Nodes (6): API models, Contrato espacial — GIS/planos/escenas, Edge cases, Endpoints, Flujo frontend, Validación

### Community 153 - "Esquema de telemetría y políticas de almacenamiento"
Cohesion: 0.29
Nodes (6): Consultas, Esquema de evento normalizado (`telemetry.observed.v1`), Esquema de telemetría y políticas de almacenamiento, Esquema StoragePolicy (`telemetry.storage-policy.v1`), Estados y métricas, Pruebas vinculantes

### Community 154 - "Docker Compose como distribución principal"
Cohesion: 0.29
Nodes (6): Build, Docker Compose como distribución principal, Roles de datos, Servicios y perfiles, Startup, Tests

### Community 155 - "Variables de entorno OAP — esquema, defaults, administración"
Cohesion: 0.29
Nodes (6): Archivo principal, Ejemplo importante, Grupos de configuración, Requisitos críticos telemetría, Variables de entorno OAP — esquema, defaults, administración, Variables y esquema validado

### Community 156 - "Rendimiento y observabilidad"
Cohesion: 0.29
Nodes (6): Alerta de saturación, BD, Carga reproducible, GIS/UI, Instrumentación, Rendimiento y observabilidad

### Community 157 - "Pruebas de seguridad negativas — por ruta/protocolo"
Cohesion: 0.29
Nodes (6): Authorization multitenancy, Commands/AI, Criterio de aprobación, DevSecOps, Pruebas de seguridad negativas — por ruta/protocolo, Web/app

### Community 158 - "Extracción de grafo de código de repositorios de referencia"
Cohesion: 0.29
Nodes (6): Extracción de grafo de código de repositorios de referencia, Fuente Atlas Java/Spring + React, Fuente OpenRemote Java/Gradle, Objetivos, Quality Gate, Resultados

### Community 159 - "Análisis de acercamiento a las normativas (81346 / Haystack / Brick / RDF-SHACL)"
Cohesion: 0.29
Nodes (6): 1. IEC/ISO 81346 (RDS por aspectos =/-/+/%), 2. Project Haystack (tags) y Xeto, 3. Brick Schema (ontología), 4. RDF y SHACL, Análisis de acercamiento a las normativas (81346 / Haystack / Brick / RDF-SHACL), Conclusión

### Community 161 - ".run_forever"
Cohesion: 0.67
Nodes (5): on_connect(), on_disconnect(), on_message(), subscribe_bindings(), sync()

### Community 166 - "Contexto persistente para Kilo Code: Open Asset Platform"
Cohesion: 0.33
Nodes (5): Contexto persistente para Kilo Code: Open Asset Platform, Decisiones cerradas, Interpretaciones de alcance, Leer antes de codificar, Objetivo innegociable

### Community 167 - "ADR: Navegación por bounded context y Conectividad como tipo de activo "Gateway""
Cohesion: 0.33
Nodes (5): ADR: Navegación por bounded context y Conectividad como tipo de activo "Gateway", Alternativas consideradas, Consecuencias, Contexto, Decisión

### Community 168 - "ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes"
Cohesion: 0.33
Nodes (5): ADR: Dashboards con widget de mapa (plano + geo) y escenas GIS por imágenes, Alternativas consideradas, Consecuencias, Contexto, Decisión

### Community 169 - "ADR: Representación visual de activos e i18n estructural"
Cohesion: 0.33
Nodes (5): ADR: Representación visual de activos e i18n estructural, Alternativas consideradas, Consecuencias, Contexto, Decisión

### Community 170 - "ADR: Jerarquía de activos, activos de ubicación y navegación arbórea"
Cohesion: 0.33
Nodes (5): ADR: Jerarquía de activos, activos de ubicación y navegación arbórea, Alternativas consideradas, Consecuencias, Contexto, Decisión

### Community 171 - "ADR: Stack semántico (81346 + Brick/Haystack + RDF/SHACL)"
Cohesion: 0.33
Nodes (5): ADR: Stack semántico (81346 + Brick/Haystack + RDF/SHACL), Alternativas consideradas, Consecuencias, Contexto, Decisión

### Community 172 - "ADR: Dashboards tipo ThingsBoard + objeto Tendencia"
Cohesion: 0.33
Nodes (5): ADR: Dashboards tipo ThingsBoard + objeto Tendencia, Alternativas consideradas, Consecuencias, Contexto, Decisión

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

### Community 198 - "Integración ERP por requisición técnica"
Cohesion: 0.40
Nodes (4): Consistencia, Contrato outbound, Estado replicated inbound, Integración ERP por requisición técnica

### Community 199 - "Catálogo de eventos versionados"
Cohesion: 0.40
Nodes (4): Catálogo de eventos versionados, Envelope común, Eventos iniciales y owners, Evolución

### Community 200 - "Política de licencias FOSS, ingeniería limpia y publicación GitHub"
Cohesion: 0.40
Nodes (4): Auditoría obligatoria, Entregables previos a release, Gate, Política de licencias FOSS, ingeniería limpia y publicación GitHub

### Community 201 - "Plugin manifest — `ai_assistant`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `ai_assistant`, Versión, datos y garantías

### Community 202 - "Plugin manifest — `analytics`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `analytics`, Versión, datos y garantías

### Community 203 - "Plugin manifest — `bacnet`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `bacnet`, Versión, datos y garantías

### Community 204 - "Plugin manifest — `bms`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `bms`, Versión, datos y garantías

### Community 205 - "Plugin manifest — `cmms`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `cmms`, Versión, datos y garantías

### Community 206 - "Plugin manifest — `dashboards`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `dashboards`, Versión, datos y garantías

### Community 207 - "Plugin manifest — `edge`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `edge`, Versión, datos y garantías

### Community 208 - "Plugin manifest — `ems`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `ems`, Versión, datos y garantías

### Community 209 - "Plugin manifest — `erp`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `erp`, Versión, datos y garantías

### Community 210 - "Plugin manifest — `http_ws`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `http_ws`, Versión, datos y garantías

### Community 211 - "Plugin manifest — `inventory`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `inventory`, Versión, datos y garantías

### Community 212 - "Plugin manifest — `mcp_server`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `mcp_server`, Versión, datos y garantías

### Community 213 - "Plugin manifest — `modbus`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `modbus`, Versión, datos y garantías

### Community 214 - "Plugin manifest — `mqtt`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `mqtt`, Versión, datos y garantías

### Community 215 - "Plugin manifest — `nodered`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `nodered`, Versión, datos y garantías

### Community 216 - "Plugin manifest — `protocol_extensions`"
Cohesion: 0.40
Nodes (4): Ciclo de vida, Declaración de extensión a construir, Plugin manifest — `protocol_extensions`, Versión, datos y garantías

### Community 217 - "Definition of Done por historia y release"
Cohesion: 0.40
Nodes (4): Definition of Done por historia y release, Historia, Hito, Release

### Community 218 - "Índice de fuentes auditadas (2026-11-17)"
Cohesion: 0.40
Nodes (4): Clasificación aplicada en las matrices, Grashjs/cmms — Atlas CMMS (`06abfe35d09372ff80f889fcde73eb3cc71dc205`), openremote/core (`6d46b473d353533ccfc3938956eed145a134f2d8`), Índice de fuentes auditadas (2026-11-17)

### Community 219 - "Baselines de repositorios y estándares — fijar antes de implementar paridad"
Cohesion: 0.40
Nodes (4): Advertencia funcional, Baselines de repositorios y estándares — fijar antes de implementar paridad, Estándares y docs (sin cambio), Registro obligatorio

### Community 220 - "vitest"
Cohesion: 0.30
Nodes (4): msw, workerDirectory, @vitejs/plugin-react, vitest

### Community 221 - "SYSTEM — Principal para agentes de construcción OAP"
Cohesion: 0.40
Nodes (4): Coordinación Kilo, Entrega por historia, SYSTEM — Principal para agentes de construcción OAP, Órdenes permanentes

### Community 226 - "Cómo interpretar “reconstruir todas las funcionalidades”"
Cohesion: 0.50
Nodes (3): Auditoría y cobertura, Cómo interpretar “reconstruir todas las funcionalidades”, No sustituir completitud por atajos

### Community 227 - "Registro de contratos OpenAPI (Fase 1)"
Cohesion: 0.50
Nodes (3): Estado por módulo, Procedimiento, Registro de contratos OpenAPI (Fase 1)

### Community 228 - "Aceptación del plugin `ai_assistant` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `ai_assistant` — G8, Evidencia requerida, Negativos obligatorios

### Community 229 - "Aceptación del plugin `analytics` — G9"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `analytics` — G9, Evidencia requerida, Negativos obligatorios

### Community 230 - "Aceptación del plugin `bacnet` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `bacnet` — G7, Evidencia requerida, Negativos obligatorios

### Community 231 - "Aceptación del plugin `bms` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `bms` — G7, Evidencia requerida, Negativos obligatorios

### Community 232 - "Aceptación del plugin `cmms` — G5"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `cmms` — G5, Evidencia requerida, Negativos obligatorios

### Community 233 - "Aceptación del plugin `dashboards` — G6"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `dashboards` — G6, Evidencia requerida, Negativos obligatorios

### Community 234 - "Aceptación del plugin `edge` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `edge` — G7, Evidencia requerida, Negativos obligatorios

### Community 235 - "Aceptación del plugin `ems` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `ems` — G7, Evidencia requerida, Negativos obligatorios

### Community 236 - "Aceptación del plugin `erp` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `erp` — G8, Evidencia requerida, Negativos obligatorios

### Community 237 - "Aceptación del plugin `http_ws` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `http_ws` — G7, Evidencia requerida, Negativos obligatorios

### Community 238 - "Aceptación del plugin `inventory` — G5"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `inventory` — G5, Evidencia requerida, Negativos obligatorios

### Community 239 - "Aceptación del plugin `mcp_server` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `mcp_server` — G8, Evidencia requerida, Negativos obligatorios

### Community 240 - "Aceptación del plugin `modbus` — G7"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `modbus` — G7, Evidencia requerida, Negativos obligatorios

### Community 241 - "Aceptación del plugin `mqtt` — G4"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `mqtt` — G4, Evidencia requerida, Negativos obligatorios

### Community 242 - "Aceptación del plugin `nodered` — G8"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `nodered` — G8, Evidencia requerida, Negativos obligatorios

### Community 243 - "Aceptación del plugin `protocol_extensions` — G9"
Cohesion: 0.50
Nodes (3): Aceptación del plugin `protocol_extensions` — G9, Evidencia requerida, Negativos obligatorios

### Community 244 - "Puertas de calidad G0–G9 — fail-closed"
Cohesion: 0.50
Nodes (3): Bloqueos explícitos, Comandos mínimos propuestos una vez que exista código, Puertas de calidad G0–G9 — fail-closed

### Community 245 - "Casos deterministas para almacenar solo cambios y máximo N/T"
Cohesion: 0.50
Nodes (3): Casos deterministas para almacenar solo cambios y máximo N/T, Fixture generator, Load test

### Community 246 - "manifest.json"
Cohesion: 0.50
Nodes (3): files, kit_version, purpose

## Knowledge Gaps
- **1204 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+1199 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1733 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **102 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Gateway` connect `Gateway` to `CanAdapter`, `platforms/views.py`, `telemetry/views.py`, `AttributeTelemetryViewSet`, `test_connectivity.py`, `AssetViewSet`, `connectivity/views.py`, `test_test_connection_waits_for_connack`, `ModbusAdapter`, `BaseAdapter`, `Dashboard`, `purge_project.py`, `assets/views.py`, `Command`, `connectivity/admin.py`, `GatewayBinding`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Gateway` (e.g. with `AssetViewSet` and `BacnetAdapter`) actually correct?**
  _`Gateway` has 32 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Migration`, `Migration`, `Migration` to the rest of the system?**
  _1204 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `django_db` be split into smaller, more focused modules?**
  _Cohesion score 0.05660377358490566 - nodes in this community are weakly interconnected._
- **Why does `Membership` connect `platforms/views.py` to `UUIDPkModel`, `dashboards/views.py`, `viewsets.py`, `core/serializers.py`, `Tenant`, `AttributeTelemetryViewSet`, `AssetViewSet`, `spatial/views.py`, `conftest.py`, `assets/views.py`, `telemetry/views.py`, `User`, `TenantScopedViewSet`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `Asset` (e.g. with `build_graph()` and `AssetSerializer`) actually correct?**
  _`Asset` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Should `endpoints.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.07801418439716312 - nodes in this community are weakly interconnected._