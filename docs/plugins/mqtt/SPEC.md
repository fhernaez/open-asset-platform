# Plugin `mqtt` — especificación funcional y técnica

**Gate de aceptación:** G4. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Conexión directa de agentes MQTT a brokers y devices; tópicos, JSONPath, transforms declarativas, shadow/current state, configuración de muestreo y persistencia sin Node-RED.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `telemetry`
- `rules`
- `commands`
- `identity`
- `events`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `MqttAgent(id, tenant, broker_config_id, subscription_defs, storage_policy_defaults, connection_status)`
- `BrokerConnection(host,port,tls,credentials_secret_ref,client_id,acl_scope)`
- `MqttBinding(asset_id,attribute_id,subscribe_topic,publish_topic,json_path,qos,retain_policy)`
- `MqttDiscoveryTemplate(topic_pattern,device_id_mapping,attribute_schema,approval_required)`
- `MqttSubscriptionHealth(agent,connectivity,received,published,backpressure)`

## Historias de usuario y workflows de extremo a extremo
1. Admin registra broker TLS/ACL y agente con defaults on_change + N/1h; configura topic JSONPath y prueba preview sin escribir histórico.
2. El broker entrega payload -> validate/schema/type/unit -> current+rules -> StoragePolicy -> PostgreSQL; el agente no delega sampling en Node-RED.
3. Publish de command solamente mediante CommandService, topics allowlisted, TTL, retries y ACK si disponible.
4. Autodiscovery crea propuesta de assets/attributes, no provisiona a tenant ni publica comandos sin confirmación.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/mqtt/brokers` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mqtt/agents` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mqtt/agents/{id}/bindings` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mqtt/agents/{id}/storage-policy` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mqtt/agents/{id}:test-connection` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mqtt/agents/{id}:discover` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Wizard broker TLS/client id/secret reference y test connection sin revelar secret.
- Pantalla MQTT Agent Storage defaults: on_change, abs/rel tolerance, N por período, window strategy, heartbeat y métricas.
- Editor atributo `storageDatapoint`, inherit/override, effective policy y vista de reducción de history.

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_MQTT_DEFAULT_ENABLED`
- `MQTT_DEFAULT_TLS_REQUIRED`
- `MQTT_BROKER_URL`
- `MQTT_CONNECT_TIMEOUT_SECONDS`
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
