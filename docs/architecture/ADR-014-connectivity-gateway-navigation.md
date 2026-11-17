# ADR: Navegación por bounded context y Conectividad como tipo de activo "Gateway"

Estado: **Aceptada** (2026-11-17).

## Contexto

La navegación actual del frontend mezcla conceptos (una entrada "MQTT" como sección propia) y no está definida en la arquitectura. La auditoría de ThingsBoard/EdgeX/Node-RED/Grafana (ver `docs/research/RESEARCH_PATTERNS.md`) y de OpenRemote muestra que la conectividad es una capacidad transversal de los activos, no un menú propio: en OpenRemote los agentes son atributos de activo (`AgentLink`), en ThingsBoard los transports viven en device profiles + integraciones, y en EdgeX hay un device service por protocolo con devices/profiles.

## Decisión

1. **Menú de 10 secciones** definido aquí y en `MASTER_ARCHITECTURE.md`, del que se deriva `frontend/src/features/flags.ts` y los prompts:
   1. Activos · 2. Conectividad · 3. Telemetría · 4. Dashboards · 5. Mapas · 6. Reglas · 7. CMMS · 8. Integraciones · 9. IA/MCP · 10. Administración.
2. **Gateway como tipo de activo especial:** un activo cuyo `AssetType` es `gateway` lleva atributos de conexión tipados (protocolo, host, puerto, TLS, secreto, polling). Se crea desde Activos o desde Conectividad indistintamente.
3. **Nueva app Django `connectivity`** (reemplaza la app `mqtt` vía migración de datos):
   - `Gateway`: activo+tenant+proyecto, `protocol` (mqtt/modbus/opcua/bacnet/snmp/can), config JSON, status.
   - `GatewayBinding`: gateway→asset→attribute, `address` (topic/registro/nodo), `mapping` (JSONPath), qos/polling, retención.
   - Worker único multi-adapter registrado por protocolo; cada adapter traduce a eventos y llama al pipeline de ingesta (`telemetry.storage.ingest_event`).
4. **Módulo de requisitos `OAP-CON`** (navegación, gateways, bindings, adapters); `OAP-MQT-*` pasa a ser alias legado de `OAP-CON-*`.

## Consecuencias

- La app `mqtt` existente migra: `BrokerConnection`+`MqttAgent` → `Gateway` (protocol `mqtt`), `MqttBinding` → `GatewayBinding`. Se conserva compatibilidad de URLs `/api/v1/mqtt/*` durante una release (alias) y luego se depreca.
- El menú deja de tener "MQTT"; Conectividad administra gateways de cualquier protocolo.
- Los adapters OPC-UA/BACnet/SNMP/CAN quedan `SPECIFIED` (gate G9) hasta implementarse; solo MQTT (P0) y Modbus (P1) se construyen primero.

## Alternativas consideradas

- Device services separados por protocolo (EdgeX-like): microservicios adicionales, más operación; rechazado para este producto.
- Mantener MQTT como menú propio: rechazado (visión del usuario confirmada).
