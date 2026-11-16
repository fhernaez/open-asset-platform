# CORE / Rules Alarms

## Objetivo de producto y límites de propiedad
Motor declarativo de reglas, alertas y automatización con scheduler y templates versionados, sin ejecutar código arbitrario de usuarios.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `RuleDefinition(trigger, conditions, action refs, revision, enabled)`.
- `RuleExecution(event_id, rule_id, state, outputs)`.
- `AlarmDefinition(metric, threshold, deadband, duration, severity)`.
- `AlarmInstance(state=new|acknowledged|cleared, timestamps, actor)`.
- `Schedule(timezone, RRULE/cron, conflicts)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `POST/GET/PATCH /api/v1/rules`.
- `POST /api/v1/rules/{id}:simulate`.
- `GET/POST /api/v1/alarms`.
- `POST /api/v1/alarms/{id}:ack`.
- `GET /api/v1/rules/{id}/executions`.

## Invariantes funcionales / reglas de negocio
- Reglas procesan todos los eventos válidos incluso filtrados de Timescale.
- Cuando-Entonces declarativo y seguridad en executor; JS/Groovy de referencia se reescriben con DSL segura, no eval bruto.
- Hysteresis, debounce, alarm flood suppression, silence windows y offline detection.
- Schedules respetan IANA timezone y DST; no duplicar trabajos.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/Timescale/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Alarma se genera con cambio aunque history no guarde por N/T.
- [ ] Misma alarma 1000 veces no crea 1000 tickets.
- [ ] Regla disabled y schedule conflict no ejecutan acción.
- [ ] Simulación no produce comandos reales.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
