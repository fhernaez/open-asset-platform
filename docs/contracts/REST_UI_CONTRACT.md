# REST, realtime y frontend plugin contract

## Convenciones
Rutas `/api/v1/<domain>`, `snake_case` JSON o estrategia consistente documentada; UUID e ISO8601 UTC; paginación cursor; filtros whitelist; If-Match para updates; versionado OpenAPI generado desde DRF; errores Problem Details uniformes con request_id. Uso consistente de 400/401/403/404/409/422/429/503.

Reglas vinculantes adicionales (2026-11-18):
- **DELETE responde 204 sin body**: el cliente debe manejar respuestas sin cuerpo (no parsear JSON en 204/empty).
- Sanitización de entradas técnicas (direcciones/topics): el backend elimina caracteres de control (`\x00`–`\x1f`) y recorta espacios.
- Media: imágenes de escenas GIS vía multipart; se sirven por `/media/` (nginx → api).
- i18n: resolución de locale usuario → organización → `OAP_DEFAULT_LOCALE` (env del servicio frontend); timezone idem (`OAP_DEFAULT_TIMEZONE`). El contenedor frontend sirve `/config.js` (window.__OAP_CONFIG__) generado por envsubst.
- Identificadores únicos: todos los campos de tipo slug/code/external_ref se presentan como **"Código"** con el mismo helper y se auto-sugieren desde el nombre (slug minúsculas/guiones); si el usuario lo edita manualmente, no se pisa.
- Alta de gateways: `POST /assets/assets/` con `gateway_config` crea Asset+Gateway atómicamente y devuelve `gateway_id`; `test-connection` intenta conexión REAL (MQTT) o responde `not_implemented`.
- Asociación activo→gateway: `POST /assets/assets/` acepta `gateway_id` opcional → crea binding `device` en la misma transacción.

## Seguridad
Auth principal local/Keycloak OIDC; CSRF para cookies, CORS allowlist, JWT audience+issuer para bearer; roles/tenant/project/object permission en cada endpoint. No exponer full table scans ni campos sensibles en list view. WebSocket/SSE los mismos filtros autorizados; cache invalidación según revocación.

## Frontend shell
React TS con routes por `UIExtensionManifest` compilado, no script remotos arbitrarios. Component registry semver, i18n es/en, dynamic AssetType forms, plugin admin, telemetry current/history, mapa local/GIS, work orders, dashboard builder, assistant opt-in. Cada pantalla tiene empty/loading/failed/offline, validación formularios y retry seguro.

## Pruebas mínimas
OpenAPI schema se parsea; TS client generated sin errores; permission matrix en REST+WS+UI; pagination; tests XSS/CSRF; Playwright workflow asset-to-MQTT-chart y admin config persists restart.
