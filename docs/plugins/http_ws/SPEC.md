# Plugin `http_ws` — especificación funcional y técnica

**Gate de aceptación:** G7. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Agentes HTTP/REST, websocket, webhook y polling de APIs; parser/mapper tipado por atributo y seguridad SSRF.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `telemetry`
- `identity`
- `events`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `HttpAgent(base_url,method,auth_secret_ref,timeout,retry)`
- `HttpBinding(json_path,point_id,interval,headers_template)`
- `WebhookEndpoint(token_hash,allowed_sources,tenant,project)`
- `WsAgent(connection_url,subscription,heartbeat)`

## Historias de usuario y workflows de extremo a extremo
1. Configurar URL y método, comprobar allowlist DNS/IP/https y auth secret reference.
2. Poll y parse JSONPath a atributos; respetar las mismas StoragePolicy que MQTT.
3. Webhook firmado valida origen, timestamp, replay, proyecto y schema.
4. WebSocket reconnect con backoff y carga acotada.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/http/agents` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/http/agents/{id}:test` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/ingest/webhooks/{token_id}` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Configurar endpoint seguro, mapping y preview de payload
- Estado conex/retry, logs sin body sensible

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_HTTP_DEFAULT_ENABLED`
- `HTTP_CONNECTOR_ALLOWED_HOSTS`
Los defaults se importan ONCE a PostgreSQL; las preferencias administrables se editan en GUI y persisten al reinicio. Secret references no exponen credenciales. Los flags locked de deploy prevalecen.

## Riesgos específicos
- Una integración puede estar ausente, lenta o mal configurada: el CORE debe mantenerse operativo.
- Cambios de contrato requieren versionado, migraciones compatibles y regresión E2E; no modificar definiciones de activos ajenas.
- Para controles físicos aplicar `CommandService`, aprobación y tests en simulador; no ejecutar hardware real como parte del CI.
- Una capacidad listada no se considera implementada sin pruebas que ejerciten su efecto observable en base real/UI.

## Documentos vinculados
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/contracts/PLUGIN_CONTRACT.md`, `docs/contracts/EVENT_CATALOG.md`, `docs/quality/GATES.md`
- `{base}/ACCEPTANCE.md`
