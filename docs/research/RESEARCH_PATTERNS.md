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

- **Representación visual de activos (3 capas):** OpenRemote `ui/component/or-icon` (icono por tipo de activo en el árbol), ThingsBoard (icono de tipo + imagen de entidad usada en el widget de mapa por imagen), Node-RED (icono SVG por tipo de nodo). Color/badge por estado es ubicuo (alarmas/estado). → OAP: icono por tipología + imagen por activo + estado derivado (ADR-016).
- **Tipologías por código:** Node-RED (nodos custom como paquetes de código) y ThingsBoard (solution templates/devices profiles) convergen en "definición declarativa versionada + catálogo semilla". → OAP: manifiestos `ASSET_TYPE_SCHEMA` + `seed_asset_types` (ADR-016).

### Tabla tipo→fuente del catálogo semilla

| Tipos | Fuente de referencia |
|---|---|
| building, room, thermostat, ventilation, light, plug, door, presence-sensor, environment-sensor, weather, people-counter, parking, gateway | OpenRemote `model/src/main/java/org/openremote/model/asset/impl/` (descriptores verificados: BuildingAsset, RoomAsset, ThermostatAsset, VentilationAsset, LightAsset, PlugAsset, DoorAsset, PresenceSensorAsset, EnvironmentSensorAsset, WeatherAsset, PeopleCounterAsset, ParkingAsset, GatewayAsset) |
| ahu, vav, fcu, boiler, chiller, pump, fan | Brick/Haystack (puntos por equipo) + dominio HVAC (NR; OpenRemote no incluye estos equipos como descriptores) |
| electricity-meter, water-meter, heat-meter, lighting-zone | Brick/Haystack + dominio (NR) |
| connection_schema de gateway-mqtt/modbus/opcua/bacnet/snmp/can | OpenRemote `agent/protocol/*` + EdgeX device services (patrones de configuración) |

Los atributos por defecto (con unidad, store y tags Brick) son el punto de partida "completo" y customizable; el seed guarda `catalog_version` y `--refresh` actualiza solo tipos no customizados (`schema.custom=true` los excluye).
- **ThingsBoard Alarm/RuleChain:** alarmas con severidad + acknowledge y reglas en cadena (equivalente OAP-RUL).
- **ThingsBoard Entity relations / EdgeX profiles:** metadatos y relaciones entre entidades (equivalente OAP-ASS relaciones y designaciones).
- **Node-RED:** catálogo core verificado (mqtt, httpin/request, websocket, tcpin, udp, tls, parsers); Modbus/OPC-UA/BACnet son nodos comunitarios, no core → OAP-NRD import/export debe prever nodos comunitarios vía mapping documentado.

## 5. Licencias (para auditoría OAP-FOSS)

- ThingsBoard: BUSL-1.1 (source-available; cada release pasa a Apache-2.0 a los 4 años). Patrón de referencia solamente.
- Grafana: AGPL-3.0. Patrón de referencia solamente.
- EdgeX (compose + device services): Apache-2.0. Patrón de referencia.
- Node-RED: Apache-2.0. Patrón de referencia; integración por API/JSON, no código embebido.
