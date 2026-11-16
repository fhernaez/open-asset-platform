# Plugin `bms` — especificación funcional y técnica

**Gate de aceptación:** G7. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Building Management System propio: equipos/áreas, HVAC, iluminación, horarios, escenas, setpoints, supervisión, alarmas y control autorizado.

## Dependencias (contratos públicos; no imports privados)
- `assets`
- `semantics`
- `spatial`
- `commands`
- `rules`
- `telemetry`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `BuildingSystem(type,asset_ref,served_zones)`
- `ControlProfile(schedule,deadband,limits,states)`
- `BmsScene(actions,conditions,approval_policy)`
- `OperatingMode(auto|manual|standby,ttl)`
- `EquipmentAvailability(asset,quality,operation_status)`

## Historias de usuario y workflows de extremo a extremo
1. Crear building/floor/zones y equipos, vincular puntos Brick/Haystack y ubicación de planos.
2. Widget HVAC muestra temp/mode/setpoint/alarms y permite propuesta de cambio validada.
3. Planificador horario decide comandos con interlocks/roles y registro de ejecución.
4. Alarmas y mantenimiento generan orden sugerida sin duplicación al repetirse un trigger.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/bms/systems` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/bms/zones` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/bms/scenes` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/bms/schedules` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/bms/commands:propose` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Plano interactivo con unidades, colores por calidad y zoom; lista de equipos HVAC/lighting
- Editor seguro schedules, operating modes y vista de alarmas

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_BMS_DEFAULT_ENABLED`
- `BMS_COMMANDS_DEFAULT_MODE`
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
