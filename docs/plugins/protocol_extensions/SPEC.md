# Plugin `protocol_extensions` — especificación funcional y técnica

**Gate de aceptación:** G9. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Adaptadores opcionales para SNMP, KNX, OPC UA, Zigbee2MQTT, TCP/UDP, WebSocket y gateways industriales, implementados progresivamente con pruebas por protocolo.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `telemetry`
- `identity`
- `commands`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `ProtocolDriverManifest(protocol,version,license,capabilities)`
- `ConnectionProfile(driver,secret_ref,params)`
- `PointMapping(external_key,asset_attribute,transform)`
- `ProtocolHealth(driver,latency,errors,last_seen)`

## Historias de usuario y workflows de extremo a extremo
1. Elegir driver de catálogo validado y configurar red/dispositivo, no ejecutar auto-discovery indiscriminado.
2. Mapear datos a AssetAttribute con unidades/calidad, respetar StoragePolicy genérica y commands seguros.
3. Proveer implementación nativa cuando sea viable o gateway de protocolo documentado sin hacer dependiente la app de Node-RED.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/protocols/drivers` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/protocols/connections` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/protocols/connections/{id}:discover` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Catálogo de drivers con estado de implementación real, protocolos y salud
- Test connection y mapping por campo

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_PROTOCOL_EXT_DEFAULT_ENABLED`
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
