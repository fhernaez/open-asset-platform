# Índice de fuentes auditadas (2026-11-17)

Inventario por paths de los repos de referencia. Los commits fijados están en `REFERENCE_LOCK.md`. El grafo completo de dependencias (nodes.csv/edges.csv vía jdeps/Gradle/AST) es una tarea posterior según `CODE_GRAPH_RUNBOOK.md`.

## openremote/core (`6d46b473d353533ccfc3938956eed145a134f2d8`)

Estructura raíz: `agent/`, `manager/`, `model/`, `model-util/`, `profile/`, `ui/`, `container/`, `deployment/`, `test/`, `tools/`. Módulos Gradle incluidos dinámicamente desde `settings.gradle`.

| Dominio | Paths verificados | Conteo notable |
|---|---|---|
| Protocol agents | `agent/src/main/java/org/openremote/agent/protocol/` | 19 adaptadores: artnet, bluetooth, http, io, knx, lorawan, mail, modbus, mqtt, openweathermap, serial, simulator, snmp, tcp, tradfri, udp, velbus, websocket, zwave |
| Manager services | `manager/src/main/java/org/openremote/manager/` | 24: agent, alarm, app, apps, asset, dashboard, datapoint, event, gateway, map, mqtt, notification, persistence, provisioning, rules, security, services, setup, simulator, syslog, system, web, webhook |
| Model | `model/src/main/java/org/openremote/model/` | 30 dominios: alarm, apps, asset, attribute, auth, calendar, console, dashboard, datapoint, event, file, flow, gateway, geo, http, mail, map, notification, persistence, protocol, provisioning, query, rules, security, services, simulator, syslog, system, util, validation, value, webhook |
| Asset | `model/.../asset/` | Asset, AssetDescriptor, AssetTree(+Asset,Node,Event), AssetTypeInfo, UserAssetLink, AssetResource |
| Attribute | `model/.../attribute/` | Attribute, AttributeState, AttributeLink, AttributeRef, AttributeExecuteStatus, AttributeWriteResult, MetaItem/MetaMap |
| Datapoint | `model/.../datapoint/` | Datapoint, AssetDatapoint, ValueDatapoint, DatapointInterval, DatapointPeriod, query/ (agregación periódica), DatapointExportFormat |
| Rules | `model/.../rules/` | Ruleset (Global/Realm/Asset), AssetRuleset, Alarms, RulesEngineInfo/Status, Notifications, Webhooks, geofence/, flow/ |
| Flow editor (JSON) | `model/.../flow/` | Flow, Node, Wire, Slot, catalog/ (editor de flujos declarativo) |
| Dashboards | `model/.../dashboard/` | Dashboard, DashboardWidget, DashboardTemplate, DashboardGridItem, DashboardAccess |
| Gateway | `model/.../gateway/` | GatewayConnection, GatewayClientResource, GatewayTunnel, GatewayAssetSyncRule, capabilities |
| Provisioning | `model/.../provisioning/` | X509ProvisioningConfig/Data/Messages, ProvisioningResource |
| Map/GIS | `model/.../map/`, `model/.../geo/` | GeoJsonConfig, MapResource |
| Alarm | `model/.../alarm/` | Alarm, AlarmAssetLink, AlarmResource, SentAlarm |
| Manager UI pages | `ui/app/manager/src/pages/` | 17 páginas: account, alarms, assets, configuration, export, gateway, gateway-tunnel, insights, logs, map, notifications, provisioning, realms, roles, rules, services, users |
| UI components | `ui/component/` | asset-tree, asset-viewer, attribute-{barchart,card,history,input,picker}, chart, dashboard-builder, gauge, json-forms, log-viewer, map, rules, scheduler, tree-menu |

## Grashjs/cmms — Atlas CMMS (`06abfe35d09372ff80f889fcde73eb3cc71dc205`)

Stack: Spring Boot (`api/`), React+TS (`frontend/`), React Native (`mobile/`), Postgres + MinIO, JWT. Licencia dual: AGPLv3 (abierta) + Comercial (`COMMERCIAL_LICENSE.MD`, INTELLOOP LLC).

| Dominio | Paths verificados | Conteo notable |
|---|---|---|
| Controllers | `api/src/main/java/com/grash/controller/` | 66: WorkOrder(+Category,+Configuration,+History,+MeterTrigger,+RequestConfiguration), Request(+Portal), PreventiveMaintenance, Asset(+Category,+Downtime), Part(+Category,+Quantity), PurchaseOrder(+Category), Location, Meter(+Category), Reading, Team, Role, User(+Settings), Vendor, Customer, Labor, TimeCategory, CostCategory, AdditionalCost, Checklist, Comment, File, FloorPlan, Workflow, Schedule, ShiftConfiguration, Notification, Webhook(+Endpoint), CustomField, FieldConfiguration, UiConfiguration, Company(+Settings), GeneralPreferences, InstanceConfig, Export, Import, Subscription(+Plan), License, ApiKey, Auth, analytics/{Asset,Part,Request,User,WO}Analytics, Workload, zapier, Paddle, Demo, HealthCheck, Deprecation, Review, Relation |
| Entidades | `api/src/main/java/com/grash/model/` | 50+: Asset, WorkOrder, Request, PreventiveMaintenance, Part, PurchaseOrder, Meter, Reading, Labor, Vendor, Location, FloorPlan, Checklist, CustomField(Value), FieldConfiguration, Schedule, Shift(Configuration,Day,Exception), Team, Role, User, Company, Notification, Webhook, Subscription(Plan), File, Downtime, Transaction, Relation |
| Frontend screens | `frontend/src/content/pages/` | 21 áreas: Account, Auth/Oauth/Payment/Status; Analytics, Assets, Categories, CompanyProfile, Files, Imports, Inventory, Locations, Meters, PeopleAndTeams, PreventiveMaintenance, PurchaseOrders, Requests, Settings, Subscription, SwitchAccount, UpgradeAndDowngrade, UserProfile, VendorsAndCustomers, WorkOrders |
| Comercial (license-gated) | `service/LicenseService.java` | `hasEntitlement(LicenseEntitlement)`, `isSSOEnabled()`; white-label (LOGO_PATHS/BRAND_CONFIG/CUSTOM_COLORS), SSO, LDAP, enterprise features → requieren `LICENSE_KEY` |

## Clasificación aplicada en las matrices

- `VERIFIED_SOURCE` — código presente en el repo auditado (path listado).
- `VERIFIED_DOCS_ONLY` — documentado (README/docs) sin implementación verificable en el path auditado.
- `COMMERCIAL_UNAVAILABLE` — funcionalidad gated por licencia comercial; OAP hace implementación original sin copiar.
- `NEW_REQUIREMENT` — requisito propio de OAP (no presente en la fuente).
- `UNKNOWN` — no verificado aún.
