# Matriz de paridad — OpenRemote Core (auditada 2026-11-17, commit `6d46b473`)

Fuente fijada: `https://github.com/openremote/core` @ `6d46b473d353533ccfc3938956eed145a134f2d8`. Licencia: CDDL-1.0 + GPL-2.0 (Classpath exception) + Timescale TSL + terceros. Inventario por paths: `docs/research/GRAPH_SOURCE_INDEX.md`.

| Área | Capacidades verificadas en fuente (paths) | Estado | Destino OAP |
|---|---|---|---|
| Asset manager | `model/.../asset/`: Asset, AssetDescriptor, AssetTree(+Node), AssetTypeInfo, UserAssetLink; `ui/component/or-asset-tree`, `or-asset-viewer` | VERIFIED_SOURCE | OAP-ASS (árbol, tipos dinámicos, metadata, atributos) |
| Attributes | `model/.../attribute/`: Attribute, AttributeState, AttributeLink, AttributeRef, AttributeExecuteStatus, AttributeWriteResult, MetaItem/MetaMap | VERIFIED_SOURCE | OAP-ASS + OAP-TEL |
| Datapoints | `model/.../datapoint/`: Datapoint, AssetDatapoint, ValueDatapoint, DatapointInterval, DatapointPeriod, query/, DatapointExportFormat (agregación periódica) | VERIFIED_SOURCE | OAP-TEL (current/history/stats) |
| MQTT | `agent/.../protocol/mqtt/` | VERIFIED_SOURCE | OAP-MQT (más políticas on_change/N-T = NEW_REQUIREMENT) |
| Protocol agents | `agent/.../protocol/`: artnet, bluetooth, http, io, knx, lorawan, mail, modbus, mqtt, openweathermap, serial, simulator, snmp, tcp, tradfri, udp, velbus, websocket, zwave (19) | VERIFIED_SOURCE | OAP-PRO (priorizar MQTT/Modbus/BACnet/HTTP; el resto P2) |
| Rules | `model/.../rules/`: Ruleset (Global/Realm/Asset), Alarms, RulesEngineInfo/Status, Notifications, Webhooks, geofence/ | VERIFIED_SOURCE | OAP-RUL |
| Flow editor | `model/.../flow/`: Flow, Node, Wire, Slot, catalog/ (editor de flujos JSON) | VERIFIED_SOURCE | OAP-RUL (editor declarativo propio) |
| Dashboards | `model/.../dashboard/`: Dashboard, DashboardWidget, DashboardTemplate, DashboardGridItem, DashboardAccess; `ui/component/or-dashboard-builder`, `or-chart`, `or-gauge` | VERIFIED_SOURCE | OAP-DSH |
| Alarm | `model/.../alarm/`: Alarm, AlarmAssetLink, AlarmResource, SentAlarm; `ui/app/manager/src/pages/page-alarms` | VERIFIED_SOURCE | OAP-RUL |
| Identity | `model/.../auth/`, `.../security/`, `manager/.../security/`, pages: realms, roles, users, account | VERIFIED_SOURCE | OAP-PLT |
| Edge/gateway | `model/.../gateway/`: GatewayConnection, GatewayClientResource, GatewayTunnel, GatewayAssetSyncRule, capabilities; pages gateway, gateway-tunnel | VERIFIED_SOURCE | OAP-PRO (edge) |
| Provisioning | `model/.../provisioning/`: X509ProvisioningConfig/Data/Messages, ProvisioningResource; page provisioning | VERIFIED_SOURCE | OAP-PRO |
| Maps/GIS | `model/.../map/` (GeoJsonConfig, MapResource), `ui/component/or-map`, page-map | VERIFIED_SOURCE | OAP-GIS |
| APIs | REST (JAX-RS resources: AssetResource, AssetDatapointResource, RulesResource, AlarmResource, DashboardResource, MapResource…) + WebSocket/event bus (Events) | VERIFIED_SOURCE | OAP-PLT (OpenAPI) |
| Persistence | PostgreSQL+Timescale (TSL en LICENSE.txt); DatapointInterval/Period, queries | VERIFIED_SOURCE | OAP-TEL (PostgreSQL plano + PostGIS; ADR-013) |
| Manager UI | `ui/app/manager/src/pages/` (17): account, alarms, assets, configuration, export, gateway, gateway-tunnel, insights, logs, map, notifications, provisioning, realms, roles, rules, services, users | VERIFIED_SOURCE | Frontend OAP (rebuild total) |
| Insights app | `ui/app/insights/` (aplicación separada) | VERIFIED_SOURCE | OAP-DSH |
| Export | `model/.../datapoint/DatapointExportFormat`, page-export | VERIFIED_SOURCE | OAP-TEL |
| Notifications | `manager/.../notification/`, page-notifications | VERIFIED_SOURCE | OAP-PLT (notificaciones) |
| Logs | `manager/.../syslog/`, page-logs | VERIFIED_SOURCE | OAP-OPS |
| KNX/Zigbee/Z-Wave y otros protocolos larga cola | adaptadores en `agent/.../protocol/` | VERIFIED_SOURCE | OAP-PRO P2 |
| Commercial/hosted OpenRemote (enterprise/cloud) | no auditado por separado | COMMERCIAL_UNAVAILABLE | implementaciones originales OAP |
| Almacenamiento solo cambios (on_change) con N/ventana T por agente/atributo | no presente como tal en la fuente auditada | NEW_REQUIREMENT | OAP-TEL (diferenciador) |
| IEC/ISO 81346 + Brick + Haystack RDF/SHACL | no presente como tal (metadata libre) | NEW_REQUIREMENT | OAP-SEM |
| Node-RED bidireccional | no presente | NEW_REQUIREMENT | OAP-NRD |
| MCP server + asistente local | no presente | NEW_REQUIREMENT | OAP-AIM |
| ERP (requisiciones) integrado | no presente (OpenRemote no incluye CMMS) | NEW_REQUIREMENT | OAP-ERP |

Regla: cada fila se declara cerrada solo cuando OAP tenga el contrato + código + test + evidencia con el ID `OAP-*` correspondiente en `TRACEABILITY.md`.
