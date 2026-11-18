"""Catálogo semilla de tipologías (formato ASSET_TYPE_SCHEMA v1).

Fuente canónica del seed: `docs/contracts/ASSET_TYPE_SCHEMA.md`. El formato de
exportación/importación (bundles) es el JSON de estos manifiestos. Seed-once
por organización: `get_or_create(tenant, code)`; upgrades solo agregan tipos.
Nombres/atributos son conceptos genéricos de dominio (patrones de OpenRemote/
ThingsBoard/EdgeX), sin copia de estructuras de repos BUSL/AGPL.
"""

from __future__ import annotations


def _attr(
    code: str,
    es: str,
    en: str,
    value_type: str = "number",
    *,
    unit: str | None = None,
    store: bool = False,
    description: tuple[str, str] | None = None,
) -> dict:
    item: dict = {
        "code": code,
        "label_i18n": {"es": es, "en": en},
        "value_type": value_type,
        "storage_datapoint": store,
    }
    if unit:
        item["unit"] = unit
    if description:
        item["description_i18n"] = {"es": description[0], "en": description[1]}
    return item


def _conn(
    field: str,
    es: str,
    en: str,
    type_: str,
    *,
    required: bool = False,
    default=None,
    options: list | None = None,
) -> dict:
    item: dict = {"field": field, "label_i18n": {"es": es, "en": en}, "type": type_, "required": required}
    if default is not None:
        item["default"] = default
    if options:
        item["options"] = [{"value": o, "label_i18n": {"es": o, "en": o}} for o in options]
    return item


MANIFESTS: list[dict] = [
    # --- Espacios ---------------------------------------------------------
    {
        "code": "building",
        "kind": "standard",
        "icon": "building",
        "label_i18n": {"es": "Edificio", "en": "Building"},
        "description_i18n": {"es": "Inmueble o edificio gestionado", "en": "Managed building or facility"},
        "attributes": [_attr("name", "Nombre", "Name", "string")],
    },
    {
        "code": "floor",
        "kind": "standard",
        "icon": "floor",
        "label_i18n": {"es": "Planta", "en": "Floor"},
        "description_i18n": {"es": "Nivel o planta de un edificio", "en": "Floor or level of a building"},
        "attributes": [_attr("name", "Nombre", "Name", "string")],
    },
    {
        "code": "room",
        "kind": "standard",
        "icon": "room",
        "label_i18n": {"es": "Sala", "en": "Room"},
        "description_i18n": {"es": "Espacio interior (habitación, sala)", "en": "Indoor space (room)"},
        "attributes": [
            _attr("temp", "Temperatura", "Temperature", unit="°C", store=True),
            _attr("humidity", "Humedad", "Humidity", unit="%", store=True),
        ],
    },
    {
        "code": "zone",
        "kind": "standard",
        "icon": "zone",
        "label_i18n": {"es": "Zona", "en": "Zone"},
        "description_i18n": {"es": "Agrupación funcional de espacios", "en": "Functional grouping of spaces"},
        "attributes": [_attr("name", "Nombre", "Name", "string")],
    },
    # --- HVAC -------------------------------------------------------------
    {
        "code": "ahu",
        "kind": "standard",
        "icon": "ahu",
        "label_i18n": {"es": "Unidad de tratamiento de aire", "en": "Air handling unit"},
        "description_i18n": {"es": "Equipo central de climatización", "en": "Central air conditioning equipment"},
        "attributes": [
            _attr("temp_supply", "Temperatura de impulsión", "Supply temperature", unit="°C", store=True),
            _attr("temp_return", "Temperatura de retorno", "Return temperature", unit="°C", store=True),
            _attr("fan_speed", "Velocidad de ventilador", "Fan speed", unit="%", store=True),
            _attr("running", "En marcha", "Running", "boolean", store=True),
        ],
    },
    {
        "code": "vav",
        "kind": "standard",
        "icon": "vav",
        "label_i18n": {"es": "Caja VAV", "en": "VAV box"},
        "description_i18n": {"es": "Caja de volumen de aire variable", "en": "Variable air volume box"},
        "attributes": [
            _attr("temp", "Temperatura", "Temperature", unit="°C", store=True),
            _attr("setpoint", "Consigna", "Setpoint", unit="°C", store=True),
            _attr("damper", "Compuerta", "Damper", unit="%", store=True),
        ],
    },
    {
        "code": "fcu",
        "kind": "standard",
        "icon": "fcu",
        "label_i18n": {"es": "Fan coil", "en": "Fan coil unit"},
        "description_i18n": {"es": "Fan coil de confort local", "en": "Local comfort fan coil"},
        "attributes": [
            _attr("temp", "Temperatura", "Temperature", unit="°C", store=True),
            _attr("setpoint", "Consigna", "Setpoint", unit="°C", store=True),
            _attr("fan_speed", "Velocidad", "Fan speed", unit="%", store=True),
        ],
    },
    {
        "code": "boiler",
        "kind": "standard",
        "icon": "boiler",
        "label_i18n": {"es": "Caldera", "en": "Boiler"},
        "description_i18n": {"es": "Generador de agua caliente", "en": "Hot water generator"},
        "attributes": [
            _attr("temp_flow", "Temperatura de ida", "Flow temperature", unit="°C", store=True),
            _attr("temp_return", "Temperatura de retorno", "Return temperature", unit="°C", store=True),
            _attr("running", "En marcha", "Running", "boolean", store=True),
        ],
    },
    {
        "code": "chiller",
        "kind": "standard",
        "icon": "chiller",
        "label_i18n": {"es": "Enfriadora", "en": "Chiller"},
        "description_i18n": {"es": "Planta enfriadora de agua", "en": "Water cooling plant"},
        "attributes": [
            _attr("temp_flow", "Temperatura de impulsión", "Supply temperature", unit="°C", store=True),
            _attr("temp_return", "Temperatura de retorno", "Return temperature", unit="°C", store=True),
            _attr("power", "Potencia", "Power", unit="kW", store=True),
            _attr("running", "En marcha", "Running", "boolean", store=True),
        ],
    },
    {
        "code": "pump",
        "kind": "standard",
        "icon": "pump",
        "label_i18n": {"es": "Bomba", "en": "Pump"},
        "description_i18n": {"es": "Bomba de impulsión", "en": "Circulation pump"},
        "attributes": [
            _attr("running", "En marcha", "Running", "boolean", store=True),
            _attr("speed", "Velocidad", "Speed", unit="%", store=True),
            _attr("power", "Potencia", "Power", unit="kW", store=True),
        ],
    },
    {
        "code": "fan",
        "kind": "standard",
        "icon": "fan",
        "label_i18n": {"es": "Ventilador", "en": "Fan"},
        "description_i18n": {"es": "Ventilador de extracción o impulsión", "en": "Extraction or supply fan"},
        "attributes": [
            _attr("running", "En marcha", "Running", "boolean", store=True),
            _attr("speed", "Velocidad", "Speed", unit="%", store=True),
        ],
    },
    # --- Energía ----------------------------------------------------------
    {
        "code": "electricity-meter",
        "kind": "standard",
        "icon": "electricity-meter",
        "label_i18n": {"es": "Medidor eléctrico", "en": "Electricity meter"},
        "description_i18n": {"es": "Medidor de energía eléctrica", "en": "Electric energy meter"},
        "attributes": [
            _attr("energy", "Energía", "Energy", unit="kWh", store=True),
            _attr("power", "Potencia", "Power", unit="kW", store=True),
        ],
    },
    {
        "code": "water-meter",
        "kind": "standard",
        "icon": "water-meter",
        "label_i18n": {"es": "Medidor de agua", "en": "Water meter"},
        "description_i18n": {"es": "Medidor de consumo de agua", "en": "Water consumption meter"},
        "attributes": [_attr("volume", "Volumen", "Volume", unit="m³", store=True)],
    },
    {
        "code": "heat-meter",
        "kind": "standard",
        "icon": "heat-meter",
        "label_i18n": {"es": "Medidor de energía térmica", "en": "Heat meter"},
        "description_i18n": {"es": "Medidor de energía térmica (kWh)", "en": "Thermal energy meter"},
        "attributes": [
            _attr("energy", "Energía", "Energy", unit="kWh", store=True),
            _attr("flow", "Caudal", "Flow", unit="m³/h", store=True),
        ],
    },
    # --- Iluminación ------------------------------------------------------
    {
        "code": "lighting-zone",
        "kind": "standard",
        "icon": "lighting-zone",
        "label_i18n": {"es": "Zona de iluminación", "en": "Lighting zone"},
        "description_i18n": {"es": "Circuito o zona de iluminación", "en": "Lighting circuit or zone"},
        "attributes": [
            _attr("on", "Encendido", "On", "boolean", store=True),
            _attr("level", "Nivel", "Level", unit="%", store=True),
        ],
    },
    # --- Gateways (kind=gateway, connection_schema) -----------------------
    {
        "code": "gateway-mqtt",
        "kind": "gateway",
        "icon": "gateway-mqtt",
        "label_i18n": {"es": "Gateway MQTT", "en": "MQTT gateway"},
        "description_i18n": {"es": "Conectividad a broker MQTT", "en": "MQTT broker connectivity"},
        "attributes": [_attr("status", "Estado de conexión", "Connection status", "string")],
        "connection_schema": [
            _conn("host", "Host", "Host", "string", required=True, default="localhost"),
            _conn("port", "Puerto", "Port", "int", required=True, default=1883),
            _conn("tls", "TLS", "TLS", "bool", default=False),
            _conn("client_id", "Client ID", "Client ID", "string"),
            _conn("username", "Usuario", "Username", "string"),
            _conn("password", "Contraseña", "Password", "secret"),
            _conn("keepalive", "Keepalive (s)", "Keepalive (s)", "int", default=60),
        ],
    },
    {
        "code": "gateway-modbus-rtu",
        "kind": "gateway",
        "icon": "gateway-modbus",
        "label_i18n": {"es": "Gateway Modbus RTU", "en": "Modbus RTU gateway"},
        "description_i18n": {"es": "Conectividad serie Modbus RTU", "en": "Modbus RTU serial connectivity"},
        "attributes": [_attr("status", "Estado de conexión", "Connection status", "string")],
        "connection_schema": [
            _conn("serial_port", "Puerto serie", "Serial port", "string", required=True, default="/dev/ttyUSB0"),
            _conn("baud", "Baudios", "Baud rate", "int", required=True, default=9600),
            _conn("parity", "Paridad", "Parity", "select", default="N", options=["N", "E", "O"]),
            _conn("stop_bits", "Bits de parada", "Stop bits", "int", default=1),
            _conn("byte_size", "Bits de datos", "Data bits", "int", default=8),
            _conn("unit_id", "Unit ID", "Unit ID", "int", required=True, default=1),
            _conn("timeout", "Timeout (s)", "Timeout (s)", "int", default=3),
        ],
    },
    {
        "code": "gateway-modbus-tcp",
        "kind": "gateway",
        "icon": "gateway-modbus",
        "label_i18n": {"es": "Gateway Modbus TCP", "en": "Modbus TCP gateway"},
        "description_i18n": {"es": "Conectividad Modbus TCP/IP", "en": "Modbus TCP/IP connectivity"},
        "attributes": [_attr("status", "Estado de conexión", "Connection status", "string")],
        "connection_schema": [
            _conn("host", "Host", "Host", "string", required=True),
            _conn("port", "Puerto", "Port", "int", required=True, default=502),
            _conn("unit_id", "Unit ID", "Unit ID", "int", required=True, default=1),
            _conn("timeout", "Timeout (s)", "Timeout (s)", "int", default=3),
        ],
    },
    {
        "code": "gateway-opcua",
        "kind": "gateway",
        "icon": "gateway-opcua",
        "label_i18n": {"es": "Gateway OPC-UA", "en": "OPC-UA gateway"},
        "description_i18n": {"es": "Conectividad OPC-UA", "en": "OPC-UA connectivity"},
        "attributes": [_attr("status", "Estado de conexión", "Connection status", "string")],
        "connection_schema": [
            _conn("endpoint_url", "Endpoint URL", "Endpoint URL", "string", required=True),
            _conn(
                "security_policy",
                "Política de seguridad",
                "Security policy",
                "select",
                default="None",
                options=["None", "Basic256Sha256", "Aes128Sha256RsaOaep"],
            ),
            _conn("username", "Usuario", "Username", "string"),
            _conn("password", "Contraseña", "Password", "secret"),
            _conn("app_uri", "Application URI", "Application URI", "string"),
        ],
    },
    {
        "code": "gateway-bacnet",
        "kind": "gateway",
        "icon": "gateway-bacnet",
        "label_i18n": {"es": "Gateway BACnet", "en": "BACnet gateway"},
        "description_i18n": {"es": "Conectividad BACnet/IP", "en": "BACnet/IP connectivity"},
        "attributes": [_attr("status", "Estado de conexión", "Connection status", "string")],
        "connection_schema": [
            _conn("device_instance", "Device instance", "Device instance", "int", required=True, default=1),
            _conn("network", "Red (IP)", "Network (IP)", "string", required=True, default="0.0.0.0/0"),
            _conn("apdu_timeout", "APDU timeout (ms)", "APDU timeout (ms)", "int", default=3000),
            _conn(
                "segmentation",
                "Segmentación",
                "Segmentation",
                "select",
                default="none",
                options=["none", "segmented", "both"],
            ),
        ],
    },
    {
        "code": "gateway-snmp",
        "kind": "gateway",
        "icon": "gateway-snmp",
        "label_i18n": {"es": "Gateway SNMP", "en": "SNMP gateway"},
        "description_i18n": {"es": "Conectividad SNMP v1/v2c/v3", "en": "SNMP v1/v2c/v3 connectivity"},
        "attributes": [_attr("status", "Estado de conexión", "Connection status", "string")],
        "connection_schema": [
            _conn("host", "Host", "Host", "string", required=True),
            _conn("port", "Puerto", "Port", "int", required=True, default=161),
            _conn(
                "version",
                "Versión",
                "Version",
                "select",
                required=True,
                default="v2c",
                options=["v1", "v2c", "v3"],
            ),
            _conn("community", "Comunidad", "Community", "string", default="public"),
            _conn("username", "Usuario (v3)", "Username (v3)", "string"),
            _conn("auth_password", "Contraseña auth (v3)", "Auth password (v3)", "secret"),
        ],
    },
    {
        "code": "gateway-can",
        "kind": "gateway",
        "icon": "gateway-can",
        "label_i18n": {"es": "Gateway CAN bus", "en": "CAN bus gateway"},
        "description_i18n": {"es": "Conectividad CAN bus", "en": "CAN bus connectivity"},
        "attributes": [_attr("status", "Estado de conexión", "Connection status", "string")],
        "connection_schema": [
            _conn("interface", "Interfaz", "Interface", "string", required=True, default="can0"),
            _conn("bitrate", "Bitrate", "Bitrate", "int", required=True, default=500000),
        ],
    },
]
