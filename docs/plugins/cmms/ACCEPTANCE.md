# Aceptación del plugin `cmms` — G5

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **CMMS-01**: Estado inválido o usuario sin rol devuelve 409/403 y no cambia.
- [ ] **CMMS-02**: Plan recurrente DST y 2 workers no crea orden duplicada.
- [ ] **CMMS-03**: Orden cerrada conserva logs/adjuntos/audit; permisos por proyecto.
- [ ] **CMMS-04**: Alarma repetida 100 veces genera 1 propuesta por incidencia.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
