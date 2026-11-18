"""Catálogo semilla de tipologías (formato ASSET_TYPE_SCHEMA v1).

Fuente canónica del seed: `docs/contracts/ASSET_TYPE_SCHEMA.md` y tabla
tipo→fuente en `docs/research/RESEARCH_PATTERNS.md`. Defaults COMPLETOS por
tipo (customizables por el usuario). Seed-once por organización
(`get_or_create(tenant, code)`); `catalog_version` + `--refresh` actualizan
solo tipos no customizados (`schema.custom=true` los excluye).
"""

from __future__ import annotations

CATALOG_VERSION = 2


def _attr(
    code: str,
    es: str,
    en: str,
    value_type: str = "number",
    *,
    unit: str | None = None,
    store: bool = False,
    brick: list[str] | None = None,
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
    if brick:
        item["metadata"] = {"brick": brick}
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


def _manifest(code: str, kind: str, icon: str, es: str, en: str, *, version: int = CATALOG_VERSION, **extra) -> dict:
    return {
        "code": code,
        "kind": kind,
        "catalog_version": version,
        "icon": icon,
        "label_i18n": {"es": es, "en": en},
        **extra,
    }


MANIFESTS: list[dict] = [
    # --- Espacios ---------------------------------------------------------
    _manifest(
        "building",
        "standard",
        "building",
        "Edificio",
        "Building",
        description_i18n={"es": "Inmueble o edificio gestionado", "en": "Managed building or facility"},
        attributes=[_attr("name", "Nombre", "Name", "string", brick=["Building"])],
    ),
    _manifest(
        "floor",
        "standard",
        "floor",
        "Planta",
        "Floor",
        description_i18n={"es": "Nivel o planta de un edificio", "en": "Floor or level of a building"},
        attributes=[_attr("name", "Nombre", "Name", "string", brick=["Floor"])],
    ),
    _manifest(
        "room",
        "standard",
        "room",
        "Sala",
        "Room",
        description_i18n={"es": "Espacio interior (habitación, sala)", "en": "Indoor space (room)"},
        attributes=[
            _attr("temp", "Temperatura", "Temperature", unit="°C", store=True, brick=["Zone_Air_Temperature_Sensor"]),
            _attr("humidity", "Humedad", "Humidity", unit="%", store=True, brick=["Humidity_Sensor"]),
            _attr("co2", "CO2", "CO2", unit="ppm", store=True, brick=["CO2_Sensor"]),
            _attr("occupancy", "Ocupación", "Occupancy", "boolean", store=True, brick=["Occupancy_Sensor"]),
        ],
    ),
    _manifest(
        "zone",
        "standard",
        "zone",
        "Zona",
        "Zone",
        description_i18n={"es": "Agrupación funcional de espacios", "en": "Functional grouping of spaces"},
        attributes=[_attr("name", "Nombre", "Name", "string", brick=["HVAC_Zone"])],
    ),
    # --- OpenRemote asset/impl -------------------------------------------
    _manifest(
        "thermostat",
        "standard",
        "thermostat",
        "Termostato",
        "Thermostat",
        description_i18n={"es": "Termostato de ambiente", "en": "Room thermostat"},
        attributes=[
            _attr("temp", "Temperatura", "Temperature", unit="°C", store=True, brick=["Zone_Air_Temperature_Sensor"]),
            _attr("setpoint", "Consigna", "Setpoint", unit="°C", store=True, brick=["Zone_Air_Temperature_Setpoint"]),
            _attr("cooling", "Refrigeración", "Cooling", "boolean", store=True, brick=["Cooling_Command"]),
            _attr("heating", "Calefacción", "Heating", "boolean", store=True, brick=["Heating_Command"]),
            _attr("mode", "Modo", "Mode", "string", store=True, brick=["Thermostat"]),
        ],
    ),
    _manifest(
        "ventilation",
        "standard",
        "ventilation",
        "Ventilación",
        "Ventilation",
        description_i18n={"es": "Unidad de ventilación", "en": "Ventilation unit"},
        attributes=[
            _attr("fan_speed", "Velocidad", "Fan speed", unit="%", store=True, brick=["Supply_Fan_Command"]),
            _attr("airflow", "Caudal", "Air flow", unit="m³/h", store=True, brick=["Supply_Air_Flow_Sensor"]),
            _attr("running", "En marcha", "Running", "boolean", store=True, brick=["Run_Status"]),
            _attr("filter_status", "Estado de filtro", "Filter status", "string", store=True, brick=["Filter_Status"]),
        ],
    ),
    _manifest(
        "light",
        "standard",
        "light",
        "Luminaria",
        "Light",
        description_i18n={"es": "Luminaria o punto de luz", "en": "Light fixture"},
        attributes=[
            _attr("on", "Encendido", "On", "boolean", store=True, brick=["On_Command"]),
            _attr("level", "Nivel", "Level", unit="%", store=True, brick=["Luminance_Command"]),
            _attr("power", "Potencia", "Power", unit="W", store=True, brick=["Electrical_Power_Sensor"]),
        ],
    ),
    _manifest(
        "plug",
        "standard",
        "plug",
        "Enchufe inteligente",
        "Smart plug",
        description_i18n={"es": "Enchufe o toma controlada", "en": "Controlled outlet"},
        attributes=[
            _attr("on", "Encendido", "On", "boolean", store=True, brick=["On_Command"]),
            _attr("power", "Potencia", "Power", unit="W", store=True, brick=["Electrical_Power_Sensor"]),
            _attr("energy", "Energía", "Energy", unit="kWh", store=True, brick=["Energy_Sensor"]),
        ],
    ),
    _manifest(
        "door",
        "standard",
        "door",
        "Puerta",
        "Door",
        description_i18n={"es": "Puerta o acceso", "en": "Door or access point"},
        attributes=[
            _attr("open", "Abierta", "Open", "boolean", store=True, brick=["Door", "Open_Status"]),
            _attr("locked", "Bloqueada", "Locked", "boolean", store=True, brick=["Lock_Status"]),
        ],
    ),
    _manifest(
        "presence-sensor",
        "standard",
        "presence-sensor",
        "Sensor de presencia",
        "Presence sensor",
        description_i18n={"es": "Sensor de presencia/ocupación", "en": "Presence/occupancy sensor"},
        attributes=[_attr("presence", "Presencia", "Presence", "boolean", store=True, brick=["Occupancy_Sensor"])],
    ),
    _manifest(
        "environment-sensor",
        "standard",
        "environment-sensor",
        "Sensor ambiental",
        "Environment sensor",
        description_i18n={"es": "Sensor ambiental multiparámetro", "en": "Multi-parameter environment sensor"},
        attributes=[
            _attr("temp", "Temperatura", "Temperature", unit="°C", store=True, brick=["Temperature_Sensor"]),
            _attr("humidity", "Humedad", "Humidity", unit="%", store=True, brick=["Humidity_Sensor"]),
            _attr("pressure", "Presión", "Pressure", unit="hPa", store=True, brick=["Pressure_Sensor"]),
            _attr("iaq", "Calidad de aire", "Air quality", "number", store=True, brick=["Air_Quality_Sensor"]),
        ],
    ),
    _manifest(
        "weather",
        "standard",
        "weather",
        "Estación meteorológica",
        "Weather station",
        description_i18n={"es": "Estación meteorológica exterior", "en": "Outdoor weather station"},
        attributes=[
            _attr("temp", "Temperatura", "Temperature", unit="°C", store=True, brick=["Weather", "Temperature_Sensor"]),
            _attr("humidity", "Humedad", "Humidity", unit="%", store=True, brick=["Humidity_Sensor"]),
            _attr(
                "wind_speed", "Velocidad del viento", "Wind speed", unit="m/s", store=True, brick=["Wind_Speed_Sensor"]
            ),
            _attr("illuminance", "Luminosidad", "Illuminance", unit="lx", store=True, brick=["Illuminance_Sensor"]),
        ],
    ),
    _manifest(
        "people-counter",
        "standard",
        "people-counter",
        "Contador de personas",
        "People counter",
        description_i18n={"es": "Conteo de personas en un acceso", "en": "Access people counting"},
        attributes=[
            _attr("count", "Conteo", "Count", "number", store=True, brick=["People_Count_Sensor"]),
            _attr("capacity", "Capacidad", "Capacity", "number", brick=["People_Count_Sensor"]),
        ],
    ),
    _manifest(
        "parking",
        "standard",
        "parking",
        "Plaza de estacionamiento",
        "Parking space",
        description_i18n={"es": "Plaza de estacionamiento", "en": "Parking space"},
        attributes=[
            _attr("occupied", "Ocupada", "Occupied", "boolean", store=True, brick=["Occupancy_Sensor"]),
            _attr("vehicle", "Vehículo detectado", "Vehicle", "boolean", store=True),
        ],
    ),
    _manifest(
        "gateway",
        "gateway",
        "gateway",
        "Gateway genérico",
        "Generic gateway",
        description_i18n={"es": "Gateway de conectividad genérico", "en": "Generic connectivity gateway"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
            _conn(
                "protocol",
                "Protocolo",
                "Protocol",
                "select",
                required=True,
                options=["mqtt", "modbus-rtu", "modbus-tcp", "opcua", "bacnet", "snmp", "can"],
            ),
            _conn("host", "Host", "Host", "string"),
            _conn("port", "Puerto", "Port", "int"),
        ],
    ),
    # --- HVAC -------------------------------------------------------------
    _manifest(
        "ahu",
        "standard",
        "ahu",
        "Unidad de tratamiento de aire",
        "Air handling unit",
        description_i18n={"es": "Equipo central de climatización", "en": "Central air conditioning equipment"},
        attributes=[
            _attr(
                "temp_supply",
                "Temperatura de impulsión",
                "Supply temperature",
                unit="°C",
                store=True,
                brick=["Supply_Air_Temperature_Sensor", "AHU"],
            ),
            _attr(
                "temp_return",
                "Temperatura de retorno",
                "Return temperature",
                unit="°C",
                store=True,
                brick=["Return_Air_Temperature_Sensor", "AHU"],
            ),
            _attr(
                "temp_outside",
                "Temperatura exterior",
                "Outside temperature",
                unit="°C",
                store=True,
                brick=["Outside_Air_Temperature_Sensor"],
            ),
            _attr(
                "humidity_supply",
                "Humedad de impulsión",
                "Supply humidity",
                unit="%",
                store=True,
                brick=["Supply_Air_Humidity_Sensor"],
            ),
            _attr(
                "pressure_supply",
                "Presión de impulsión",
                "Supply pressure",
                unit="Pa",
                store=True,
                brick=["Supply_Air_Static_Pressure_Sensor"],
            ),
            _attr(
                "fan_speed", "Velocidad de ventilador", "Fan speed", unit="%", store=True, brick=["Supply_Fan_Command"]
            ),
            _attr("running", "En marcha", "Running", "boolean", store=True, brick=["Run_Status", "AHU"]),
            _attr("filter_status", "Estado de filtro", "Filter status", "string", store=True, brick=["Filter_Status"]),
        ],
    ),
    _manifest(
        "vav",
        "standard",
        "vav",
        "Caja VAV",
        "VAV box",
        description_i18n={"es": "Caja de volumen de aire variable", "en": "Variable air volume box"},
        attributes=[
            _attr(
                "temp",
                "Temperatura",
                "Temperature",
                unit="°C",
                store=True,
                brick=["Zone_Air_Temperature_Sensor", "VAV"],
            ),
            _attr("setpoint", "Consigna", "Setpoint", unit="°C", store=True, brick=["Zone_Air_Temperature_Setpoint"]),
            _attr("airflow", "Caudal", "Air flow", unit="m³/h", store=True, brick=["Discharge_Air_Flow_Sensor"]),
            _attr("damper", "Compuerta", "Damper", unit="%", store=True, brick=["Damper_Position_Command"]),
            _attr("reheat", "Recalentamiento", "Reheat", unit="%", store=True, brick=["Reheat_Valve_Command"]),
        ],
    ),
    _manifest(
        "fcu",
        "standard",
        "fcu",
        "Fan coil",
        "Fan coil unit",
        description_i18n={"es": "Fan coil de confort local", "en": "Local comfort fan coil"},
        attributes=[
            _attr(
                "temp",
                "Temperatura",
                "Temperature",
                unit="°C",
                store=True,
                brick=["Zone_Air_Temperature_Sensor", "FCU"],
            ),
            _attr("setpoint", "Consigna", "Setpoint", unit="°C", store=True, brick=["Zone_Air_Temperature_Setpoint"]),
            _attr("fan_speed", "Velocidad", "Fan speed", unit="%", store=True, brick=["Fan_Command"]),
            _attr("valve", "Válvula", "Valve", unit="%", store=True, brick=["Water_Valve_Command"]),
            _attr("running", "En marcha", "Running", "boolean", store=True, brick=["Run_Status"]),
        ],
    ),
    _manifest(
        "boiler",
        "standard",
        "boiler",
        "Caldera",
        "Boiler",
        description_i18n={"es": "Generador de agua caliente", "en": "Hot water generator"},
        attributes=[
            _attr(
                "temp_flow",
                "Temperatura de ida",
                "Flow temperature",
                unit="°C",
                store=True,
                brick=["Supply_Water_Temperature_Sensor", "Boiler"],
            ),
            _attr(
                "temp_return",
                "Temperatura de retorno",
                "Return temperature",
                unit="°C",
                store=True,
                brick=["Return_Water_Temperature_Sensor"],
            ),
            _attr("pressure", "Presión", "Pressure", unit="bar", store=True, brick=["Water_Pressure_Sensor"]),
            _attr("power", "Potencia", "Power", unit="kW", store=True, brick=["Power_Sensor"]),
            _attr("running", "En marcha", "Running", "boolean", store=True, brick=["Run_Status"]),
            _attr("modulation", "Modulación", "Modulation", unit="%", store=True, brick=["Heating_Command"]),
        ],
    ),
    _manifest(
        "chiller",
        "standard",
        "chiller",
        "Enfriadora",
        "Chiller",
        description_i18n={"es": "Planta enfriadora de agua", "en": "Water cooling plant"},
        attributes=[
            _attr(
                "temp_flow",
                "Temperatura de impulsión",
                "Supply temperature",
                unit="°C",
                store=True,
                brick=["Chilled_Water_Supply_Temperature_Sensor", "Chiller"],
            ),
            _attr(
                "temp_return",
                "Temperatura de retorno",
                "Return temperature",
                unit="°C",
                store=True,
                brick=["Chilled_Water_Return_Temperature_Sensor"],
            ),
            _attr("power", "Potencia", "Power", unit="kW", store=True, brick=["Power_Sensor"]),
            _attr("running", "En marcha", "Running", "boolean", store=True, brick=["Run_Status"]),
            _attr("load", "Carga", "Load", unit="%", store=True, brick=["Load_Sensor"]),
        ],
    ),
    _manifest(
        "pump",
        "standard",
        "pump",
        "Bomba",
        "Pump",
        description_i18n={"es": "Bomba de impulsión", "en": "Circulation pump"},
        attributes=[
            _attr("running", "En marcha", "Running", "boolean", store=True, brick=["Run_Status", "Pump"]),
            _attr("speed", "Velocidad", "Speed", unit="%", store=True, brick=["Pump_Command"]),
            _attr("power", "Potencia", "Power", unit="kW", store=True, brick=["Power_Sensor"]),
            _attr("flow", "Caudal", "Flow", unit="m³/h", store=True, brick=["Water_Flow_Sensor"]),
            _attr("hours", "Horas de marcha", "Run hours", unit="h", store=True),
        ],
    ),
    _manifest(
        "fan",
        "standard",
        "fan",
        "Ventilador",
        "Fan",
        description_i18n={"es": "Ventilador de extracción o impulsión", "en": "Extraction or supply fan"},
        attributes=[
            _attr("running", "En marcha", "Running", "boolean", store=True, brick=["Run_Status", "Fan"]),
            _attr("speed", "Velocidad", "Speed", unit="%", store=True, brick=["Fan_Command"]),
            _attr("power", "Potencia", "Power", unit="kW", store=True, brick=["Power_Sensor"]),
        ],
    ),
    # --- Energía ----------------------------------------------------------
    _manifest(
        "electricity-meter",
        "standard",
        "electricity-meter",
        "Medidor eléctrico",
        "Electricity meter",
        description_i18n={"es": "Medidor de energía eléctrica", "en": "Electric energy meter"},
        attributes=[
            _attr("energy", "Energía", "Energy", unit="kWh", store=True, brick=["Energy_Sensor"]),
            _attr("power", "Potencia", "Power", unit="kW", store=True, brick=["Electrical_Power_Sensor"]),
            _attr("voltage", "Tensión", "Voltage", unit="V", store=True, brick=["Voltage_Sensor"]),
            _attr("current", "Corriente", "Current", unit="A", store=True, brick=["Current_Sensor"]),
        ],
    ),
    _manifest(
        "water-meter",
        "standard",
        "water-meter",
        "Medidor de agua",
        "Water meter",
        description_i18n={"es": "Medidor de consumo de agua", "en": "Water consumption meter"},
        attributes=[
            _attr("volume", "Volumen", "Volume", unit="m³", store=True, brick=["Water_Volume_Sensor"]),
            _attr("flow", "Caudal", "Flow", unit="m³/h", store=True, brick=["Water_Flow_Sensor"]),
        ],
    ),
    _manifest(
        "heat-meter",
        "standard",
        "heat-meter",
        "Medidor de energía térmica",
        "Heat meter",
        description_i18n={"es": "Medidor de energía térmica (kWh)", "en": "Thermal energy meter"},
        attributes=[
            _attr("energy", "Energía", "Energy", unit="kWh", store=True, brick=["Thermal_Energy_Sensor"]),
            _attr("flow", "Caudal", "Flow", unit="m³/h", store=True, brick=["Water_Flow_Sensor"]),
            _attr("temp_flow", "Temperatura de ida", "Flow temperature", unit="°C", store=True),
            _attr("temp_return", "Temperatura de retorno", "Return temperature", unit="°C", store=True),
        ],
    ),
    # --- Iluminación ------------------------------------------------------
    _manifest(
        "lighting-zone",
        "standard",
        "lighting-zone",
        "Zona de iluminación",
        "Lighting zone",
        description_i18n={"es": "Circuito o zona de iluminación", "en": "Lighting circuit or zone"},
        attributes=[
            _attr("on", "Encendido", "On", "boolean", store=True, brick=["Lighting_Zone", "On_Command"]),
            _attr("level", "Nivel", "Level", unit="%", store=True, brick=["Luminance_Command"]),
            _attr("power", "Potencia", "Power", unit="kW", store=True, brick=["Electrical_Power_Sensor"]),
        ],
    ),
    # --- Gateways (kind=gateway, connection_schema) -----------------------
    _manifest(
        "gateway-mqtt",
        "gateway",
        "gateway-mqtt",
        "Gateway MQTT",
        "MQTT gateway",
        description_i18n={"es": "Conectividad a broker MQTT", "en": "MQTT broker connectivity"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
            _conn("host", "Host", "Host", "string", required=True, default="localhost"),
            _conn("port", "Puerto", "Port", "int", required=True, default=1883),
            _conn("tls", "TLS", "TLS", "bool", default=False),
            _conn("client_id", "Client ID", "Client ID", "string"),
            _conn("username", "Usuario", "Username", "string"),
            _conn("password", "Contraseña", "Password", "secret"),
            _conn("keepalive", "Keepalive (s)", "Keepalive (s)", "int", default=60),
        ],
    ),
    _manifest(
        "gateway-modbus-rtu",
        "gateway",
        "gateway-modbus",
        "Gateway Modbus RTU",
        "Modbus RTU gateway",
        description_i18n={"es": "Conectividad serie Modbus RTU", "en": "Modbus RTU serial connectivity"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
            _conn("serial_port", "Puerto serie", "Serial port", "string", required=True, default="/dev/ttyUSB0"),
            _conn("baud", "Baudios", "Baud rate", "int", required=True, default=9600),
            _conn("parity", "Paridad", "Parity", "select", default="N", options=["N", "E", "O"]),
            _conn("stop_bits", "Bits de parada", "Stop bits", "int", default=1),
            _conn("byte_size", "Bits de datos", "Data bits", "int", default=8),
            _conn("unit_id", "Unit ID", "Unit ID", "int", required=True, default=1),
            _conn("timeout", "Timeout (s)", "Timeout (s)", "int", default=3),
        ],
    ),
    _manifest(
        "gateway-modbus-tcp",
        "gateway",
        "gateway-modbus",
        "Gateway Modbus TCP",
        "Modbus TCP gateway",
        description_i18n={"es": "Conectividad Modbus TCP/IP", "en": "Modbus TCP/IP connectivity"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
            _conn("host", "Host", "Host", "string", required=True),
            _conn("port", "Puerto", "Port", "int", required=True, default=502),
            _conn("unit_id", "Unit ID", "Unit ID", "int", required=True, default=1),
            _conn("timeout", "Timeout (s)", "Timeout (s)", "int", default=3),
        ],
    ),
    _manifest(
        "gateway-opcua",
        "gateway",
        "gateway-opcua",
        "Gateway OPC-UA",
        "OPC-UA gateway",
        description_i18n={"es": "Conectividad OPC-UA", "en": "OPC-UA connectivity"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
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
    ),
    _manifest(
        "gateway-bacnet",
        "gateway",
        "gateway-bacnet",
        "Gateway BACnet",
        "BACnet gateway",
        description_i18n={"es": "Conectividad BACnet/IP", "en": "BACnet/IP connectivity"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
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
    ),
    _manifest(
        "gateway-snmp",
        "gateway",
        "gateway-snmp",
        "Gateway SNMP",
        "SNMP gateway",
        description_i18n={"es": "Conectividad SNMP v1/v2c/v3", "en": "SNMP v1/v2c/v3 connectivity"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
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
    ),
    _manifest(
        "gateway-can",
        "gateway",
        "gateway-can",
        "Gateway CAN bus",
        "CAN bus gateway",
        description_i18n={"es": "Conectividad CAN bus", "en": "CAN bus connectivity"},
        attributes=[_attr("status", "Estado de conexión", "Connection status", "string")],
        connection_schema=[
            _conn("interface", "Interfaz", "Interface", "string", required=True, default="can0"),
            _conn("bitrate", "Bitrate", "Bitrate", "int", required=True, default=500000),
        ],
    ),
]
