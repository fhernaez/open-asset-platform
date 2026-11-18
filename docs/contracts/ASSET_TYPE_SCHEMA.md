# Contrato — Esquema de tipologías de activos (ASSET_TYPE_SCHEMA v1)

Formato declarativo único para tipologías de activos, definibles **por código** (manifiestos versionados en `backend/assets/types_catalog/manifests/`, sembrados con `seed_asset_types`) y, a futuro, **por UI** (el editor visual de tipologías generará este mismo formato — ADR-016). Exportable/importable (bundles P2).

## Manifiesto (YAML/JSON)

```yaml
code: ahu                      # slug único por tenant (patrón ^[a-z0-9-]+$)
kind: standard                 # standard | gateway
icon: ahu                      # clave de la librería SVG integrada (o data:image/svg+xml;base64,...)
label_i18n:                    # nombre mostrado según locale activo (mínimo es/en)
  es: "Unidad de tratamiento de aire"
  en: "Air handling unit"
description_i18n:
  es: "Equipo central de climatización"
  en: "Central air conditioning equipment"
attributes:                    # plantilla de atributos (se crean al crear un activo con esta tipología)
  - code: temp
    label_i18n: { es: "Temperatura", en: "Temperature" }
    value_type: number         # string | boolean | number | json
    unit: "°C"                 # símbolo de unidad (catálogo assets_unit)
    storage_datapoint: true    # default del atributo al crearse
    description_i18n: { es: "Temperatura de impulsión", en: "Supply air temperature" }
    metadata:                  # tags libres (Brick/Haystack/81346)
      brick: ["AHU", "Supply_Air_Temperature_Sensor"]
connection_schema:             # SOLO kind=gateway: campos de conexión del formulario/adapter
  - field: host
    label_i18n: { es: "Host", en: "Host" }
    type: string
    required: true
  - field: port
    label_i18n: { es: "Puerto", en: "Port" }
    type: int
    required: true
    default: 1883
  - field: password
    label_i18n: { es: "Contraseña", en: "Password" }
    type: secret               # se guarda como referencia a secreto, nunca en claro
    required: false
  - field: mode
    label_i18n: { es: "Modo", en: "Mode" }
    type: select
    options: [{ value: "a", label_i18n: { es: "A", en: "A" } }, { value: "b", label_i18n: { es: "B", en: "B" } }]
    default: "a"
```

## Reglas

- `code` único por tenant; `label_i18n` obligatorio con al menos el locale primario (`es`); `name` legacy = alias de `label_i18n[primario]`.
- `attributes[].code` único dentro del tipo; `unit` debe existir en `assets_unit` (se crea si falta vía seed).
- Para `kind=gateway`, `connection_schema` es obligatorio (el formulario de alta del gateway y el adapter lo consumen). Tipos de campo: `string`, `int`, `bool`, `secret`, `select`.
- `icon`: clave de `assets/icons` (librería integrada) o SVG embebido; la UI cae a un icono genérico por categoría si falta.
- El seed es **seed-once por organización**: `get_or_create(tenant, code)`; no pisa ediciones del usuario; upgrades de catálogo solo agregan tipos nuevos.

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
