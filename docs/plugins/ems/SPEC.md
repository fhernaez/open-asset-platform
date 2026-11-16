# Plugin `ems` — especificación funcional y técnica

**Gate de aceptación:** G7. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Energy Management: medición, perfiles de carga, costos/tarifas, objetivos, alertas de consumo, PV/BESS y peak shaving simulable sin mandar comandos peligrosos.

## Dependencias (contratos públicos; no imports privados)
- `telemetry`
- `assets`
- `rules`
- `dashboards`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `EnergyMeter(asset,channels,kwh_kw_units)`
- `TariffPlan(currency,timezone,periods,validity)`
- `EnergyBaseline(project,period,method)`
- `EnergyKPI(meter,interval,value,quality)`
- `DispatchScenario(load,pv,bess,constraints)`

## Historias de usuario y workflows de extremo a extremo
1. Vincular medidor y atributos energía/potencia con unidades y time zone.
2. Calcular demanda punta/fuera punta y consumo por período con calidad/no gaps silenciosos.
3. Simular PV/BESS peak shaving separado de control real, con reserva SoC y límites.
4. Alertar demanda/consumo sobre umbral y disparar mantenimiento si data quality confirma.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/ems/meters` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/ems/tariffs` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/ems/kpis` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/ems/scenarios:simulate` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Dashboard consumo/potencia/savings e información de calidad
- Editor tarifas períodos, simulación sin actuación real

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_EMS_DEFAULT_ENABLED`
- `EMS_CURRENCY_DEFAULT`
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
