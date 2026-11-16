# Plugin `modbus` — especificación funcional y técnica

**Gate de aceptación:** G7. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Modbus TCP y RTU polling/lectura/escritura, tipado de registros y coils, base 0/1 configurada, batching y salud de gateway.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `telemetry`
- `commands`
- `identity`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `ModbusAgent(transport=tcp|rtu,host,port,serial_ref,unit_id,byte_order)`
- `RegisterBinding(asset,attribute,address,address_base,kind,datatype,scale,read_interval,write_enabled)`
- `PollingGroup(agent,registers,interval,timeout,retry)`
- `ModbusHealth(agent,connected,last_success,error_count)`

## Historias de usuario y workflows de extremo a extremo
1. Crear agent TCP o RTU, mapear registro holding/input/coil a Point del activo, declarar endian/escala/intervalo.
2. Scheduler agrupa registros contiguos seguros, limita polling y convierte tipos, incluyendo signed/unsigned/float.
3. Write pasa CommandService y validador de rangos; readback/ack cuando soportado.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/modbus/agents` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/modbus/agents/{id}/registers` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/modbus/agents/{id}:diagnose` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Formulario TCP/RTU con comprobación de puerto y prueba contra simulador
- Editor de mapa de registros con base 0/1 visible, dtype, escala, unidad y preview

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_MODBUS_DEFAULT_ENABLED`
- `MODBUS_POLL_MIN_MS`
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
