# Aceptación del plugin `ems` — G7

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **EMS-01**: kW vs kWh consistencia fixture y timezone tarifaria.
- [ ] **EMS-02**: Agregación 15-min/mensual sin doble contar puntos repetidos.
- [ ] **EMS-03**: Escenario no ejecuta comandos físicos.
- [ ] **EMS-04**: Faltantes se reportan en vez de inventar consumo.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
