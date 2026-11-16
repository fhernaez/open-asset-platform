# Plugin `bacnet` — especificación funcional y técnica

**Gate de aceptación:** G7. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
BACnet/IP discovery, lectura de objetos/properties, trends COV/polling, escritura segura y mapeos Brick/Project Haystack para HVAC.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `telemetry`
- `commands`
- `semantics`
- `identity`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `BacnetAgent(device_instance,network,port,foreign_device,secret_refs)`
- `BacnetObjectBinding(object_type,instance,property_id,array_index,attribute_id)`
- `COVSubscription(device,object,expiry,retry)`
- `BacnetHealth(last_discovery,last_success,error_state)`

## Historias de usuario y workflows de extremo a extremo
1. Descubrir dispositivo en red permitida (no escanear segmentos arbitrarios) y presentar assets/properties para aprobación.
2. Leer propiedades con calidad e timestamps; COV con renewal y fallback poll controlado.
3. Writes pasan CommandService y config de prioridad BACnet documentada y auditada.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/bacnet/devices:discover` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/bacnet/devices/{id}/objects` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/bacnet/devices/{id}/bindings` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Explorador de objetos BACnet con import preview
- Configurar poll/COV, prioridad escritura, estado comunicación

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_BACNET_DEFAULT_ENABLED`
- `BACNET_ALLOWED_NETWORKS`
- `BACNET_MIN_POLL_MS`
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
