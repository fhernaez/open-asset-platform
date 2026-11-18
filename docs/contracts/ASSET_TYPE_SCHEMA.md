# Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1)

Formato declarativo único para tipologías de activos, definibles **por código** (manifiestos versionados en `backend/assets/types_catalog/manifests/`, sembrados con `seed_asset_types`) y, a futuro, **por UI** (el editor visual de tipologías generará este mismo formato — ADR-016). Exportable/importable (bundles P2).

## Manifiesto (YAML/JSON)

```yaml
code: ahu                      # slug único por tenant (patrón ^[a-z0-9-]+$)
kind: standard                 # standard | gateway
catalog_version: 2             # versión del manifiesto para seed --refresh
icon: ahu                      # clave de la librería SVG integrada (o data:image/svg+xml;base64,...)
label_i18n:                    # nombre mostrado según locale activo (mínimo es/en)
  es: "Unidad de tratamiento de aire"
  en: "Air handling unit"
description_i18n:
  es: "Equipo central de climatización"
  en: "Central air conditioning equipment"
attributes:                    # plantilla COMPLETA por defecto (customizable luego por el usuario)
  - code: temp_supply
    label_i18n: { es: "Temperatura de impulsión", en: "Supply temperature" }
    value_type: number
    unit: "°C"
    storage_datapoint: true
    metadata: { brick: ["Supply_Air_Temperature_Sensor", "AHU"] }
  - code: temp_return
    label_i18n: { es: "Temperatura de retorno", en: "Return temperature" }
    value_type: number
    unit: "°C"
    storage_datapoint: true
    metadata: { brick: ["Return_Air_Temperature_Sensor", "AHU"] }
  - code: fan_speed
    label_i18n: { es: "Velocidad de ventilador", en: "Fan speed" }
    value_type: number
    unit: "%"
    storage_datapoint: true
    metadata: { brick: ["Supply_Fan_Command"] }
  - code: running
    label_i18n: { es: "En marcha", en: "Running" }
    value_type: boolean
    storage_datapoint: true
    metadata: { brick: ["Run_Status", "AHU"] }
connection_schema:             # SOLO kind=gateway
  - field: host
    label_i18n: { es: "Host", en: "Host" }
    type: string
    required: true
```

## Reglas

- `code` único por tenant; `label_i18n` obligatorio con al menos el locale primario (`es`); `name` legacy = alias de `label_i18n[primario]`.
- `catalog_version` (int): versión del manifiesto. El seed guarda `schema.catalog_version`; `seed_asset_types --refresh` re-sincroniza tipos cuyo `catalog_version` es menor y que NO fueron customizados. Si el usuario edita el schema por API/UI, el serializer marca `schema.custom=true` y el refresh lo salta (las ediciones del usuario prevalecen).
- `attributes[].code` único dentro del tipo; `unit` debe existir en `assets_unit` (se crea si falta vía seed).
- Para `kind=gateway`, `connection_schema` es obligatorio (el formulario de alta del gateway y el adapter lo consumen). Tipos de campo: `string`, `int`, `bool`, `secret`, `select`.
- **Alta de activo gateway inline:** al crear un activo con tipología `kind=gateway`, la API acepta `gateway_config`; el backend crea el Asset + el `Gateway` (config validada contra `connection_schema`) en UNA transacción. Los activos estándar solo heredan sus atributos por defecto.
- `icon`: clave de `assets/icons` (librería integrada) o SVG embebido; la UI cae a un icono genérico por categoría si falta.
- El seed es **seed-once por organización**: `get_or_create(tenant, code)`; no pisa ediciones del usuario; upgrades de catálogo solo agregan tipos nuevos (o actualizan vía `--refresh` los no customizados).

## Schemas de conexión predefinidos (patrones de OpenRemote/EdgeX/ThingsBoard)

| Tipo gateway | Campos de conexión |
|---|---|
| `gateway-mqtt` | host, port(1883), tls(bool), client_id, username, password(secret), keepalive |
| `gateway-modbus-rtu` | serial_port, baud(9600), parity(select), stop_bits, byte_size, unit_id, timeout |
| `gateway-modbus-tcp` | host, port(502), unit_id, timeout |
| `gateway-opcua` | endpoint_url, security_policy(select), username, password(secret), app_uri |
| `gateway-bacnet` | device_instance, network, apdu_timeout, segmentation |
| `gateway-snmp` | host, port(161), version(select v1/v2c/v3), community, username, auth/priv(secret) |
| `gateway-can` | interface, bitrate |

## Representación visual (ADR-016)

- `icon` por tipología (librería SVG integrada + subida custom por tenant, P2).
- `image` opcional por activo (foto/símbolo; usada en planos/mapas/dashboards).
- Rendering de estado derivado (color/badge por status/alarma) — lo consume el widget de mapa y los overlays.

## i18n

- La UI usa react-i18next + locales AntD (es/en base); locale por organización con override por usuario (P2).
- Los datos del usuario (nombres de activos/proyectos) NO se traducen; los manifiestos sí (label_i18n/description_i18n).
