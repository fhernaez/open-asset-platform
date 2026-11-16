# REST, realtime y frontend plugin contract

## Convenciones
Rutas `/api/v1/<domain>`, `snake_case` JSON o estrategia consistente documentada; UUID e ISO8601 UTC; paginación cursor; filtros whitelist; If-Match para updates; versionado OpenAPI generado desde DRF; errores Problem Details uniformes con request_id. Uso consistente de 400/401/403/404/409/422/429/503.

## Seguridad
Auth principal local/Keycloak OIDC; CSRF para cookies, CORS allowlist, JWT audience+issuer para bearer; roles/tenant/project/object permission en cada endpoint. No exponer full table scans ni campos sensibles en list view. WebSocket/SSE los mismos filtros autorizados; cache invalidación según revocación.

## Frontend shell
React TS con routes por `UIExtensionManifest` compilado, no script remotos arbitrarios. Component registry semver, i18n es/en, dynamic AssetType forms, plugin admin, telemetry current/history, mapa local/GIS, work orders, dashboard builder, assistant opt-in. Cada pantalla tiene empty/loading/failed/offline, validación formularios y retry seguro.

## Pruebas mínimas
OpenAPI schema se parsea; TS client generated sin errores; permission matrix en REST+WS+UI; pagination; tests XSS/CSRF; Playwright workflow asset-to-MQTT-chart y admin config persists restart.
