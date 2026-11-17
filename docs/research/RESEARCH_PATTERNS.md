# Patrones extraídos de repos de referencia (2026-11-17)

Fuentes: ThingsBoard, EdgeX (compose + device services), Node-RED, Grafana, más OpenRemote/Atlas ya auditados. Commits en `REFERENCE_LOCK.md`. Regla: **solo patrones y conceptos**; cero copia de código de repos BUSL (ThingsBoard) o AGPL (Grafana/Atlas).

## 1. Navegación / menú

- **OpenRemote Manager UI:** páginas planas por área funcional (assets, alarms, rules, dashboards(insights), map, gateway, users, roles, realms, logs, export…).
- **ThingsBoard:** entidades primero (Devices, Assets, Device/Asset profiles, Integrations), luego procesamiento (Rule chains, Scheduler), visualización (Dashboards, Widgets library) y administración (Customers, Users, Settings, White-labeling).
- **Síntesis OAP (ADR-014):** menú = Activos, Conectividad, Telemetría, Dashboards, Mapas, Reglas, CMMS, Integraciones, IA/MCP, Administración. El menú se define en la arquitectura y se deriva (flags.ts, prompts) para no duplicar la decisión.

## 2. Conectividad / gateways

- **OpenRemote:** el agente es un atributo `AgentLink` sobre el atributo de un activo; protocolos como adaptadores en `agent/protocol/*`.
- **ThingsBoard:** `DeviceProfile` (transport MQTT/HTTP/CoAP/SNMP/… + processing) y **Integrations** con `ConverterLibrary` (gateways tipo Modbus/OPC-UA/MQTT → converters normalizan a atributos/telemetría).
- **EdgeX:** un **device service por protocolo** (device-mqtt, device-modbus, device-rest, device-virtual, device-snmp; NO existe device-bacnet en EdgeX) con `device profiles` (resources read/write) y `core-data` para events/readings.
- **Síntesis OAP (ADR-014):** `Gateway` como **tipo de activo** con atributos de conexión tipados (host/puerto/TLS/secreto/polling) + `GatewayBinding` genérica (gateway→atributo, dirección topic/registro, mapeo JSONPath). Un worker multi-adapter por protocolo (mqtt, modbus, opcua, bacnet, snmp, can) alimenta el pipeline de ingesta existente.

## 3. Dashboards y widgets de mapa

- **Grafana paneles (catálogo verificado):** timeseries, gauge, stat, barchart, table, heatmap, state-timeline, status-history, **canvas** (fondo de imagen = plano), **geomap** (capas geo), nodeGraph, piechart, candlestick, hist...
- **ThingsBoard widgets:** librería de widgets por bundle; mapa por imagen ("Image Map" widget = plano con dispositivos posicionados) y mapa geo (OpenStreetMap/Google).
- **Síntesis OAP (ADR-015):** builder con grid + widgets línea/gauge/card/tabla (ECharts) + **widget de mapa con dos modos**: plano (imagen con activos posicionados + overlays de estado) y geo (MapLibre). Escenas GIS por imágenes con capas; placement por clic sobre plano o lat/lng.

## 4. Otros patrones relevantes

- **ThingsBoard Alarm/RuleChain:** alarmas con severidad + acknowledge y reglas en cadena (equivalente OAP-RUL).
- **ThingsBoard Entity relations / EdgeX profiles:** metadatos y relaciones entre entidades (equivalente OAP-ASS relaciones y designaciones).
- **Node-RED:** catálogo core verificado (mqtt, httpin/request, websocket, tcpin, udp, tls, parsers); Modbus/OPC-UA/BACnet son nodos comunitarios, no core → OAP-NRD import/export debe prever nodos comunitarios vía mapping documentado.

## 5. Licencias (para auditoría OAP-FOSS)

- ThingsBoard: BUSL-1.1 (source-available; cada release pasa a Apache-2.0 a los 4 años). Patrón de referencia solamente.
- Grafana: AGPL-3.0. Patrón de referencia solamente.
- EdgeX (compose + device services): Apache-2.0. Patrón de referencia.
- Node-RED: Apache-2.0. Patrón de referencia; integración por API/JSON, no código embebido.
