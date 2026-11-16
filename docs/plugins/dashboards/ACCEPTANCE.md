# Aceptación del plugin `dashboards` — G6

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **DASHBOARDS-01**: Crear/editar/compartir dashboard E2E con reload.
- [ ] **DASHBOARDS-02**: Widget plugin deshabilitado queda placeholder sin perder configuración.
- [ ] **DASHBOARDS-03**: Sin permiso asset, widget no muestra datos sensibles.
- [ ] **DASHBOARDS-04**: Un lote 1000 sensores no causa miles requests no paginadas.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
