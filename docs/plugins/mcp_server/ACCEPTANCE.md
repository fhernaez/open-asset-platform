# Aceptación del plugin `mcp_server` — G8

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **MCP_SERVER-01**: MCP client con token sin scopes obtiene forbidden.
- [ ] **MCP_SERVER-02**: Read tool nunca entrega assets tenant ajeno.
- [ ] **MCP_SERVER-03**: Tool write sin aprobación devuelve proposal id, no changes.
- [ ] **MCP_SERVER-04**: MCP disabled no expone herramientas y no rompe CORE.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
