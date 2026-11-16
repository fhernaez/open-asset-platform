# Aceptación del plugin `nodered` — G8

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **NODERED-01**: JSON con 1 broker/2 sensors: preview correcto y commit idempotente.
- [ ] **NODERED-02**: Export JSON importable a pestaña Node-RED válida, sin credenciales.
- [ ] **NODERED-03**: Cambio manual de flow produce conflicto 409 y no sobrescribe.
- [ ] **NODERED-04**: Sin Node-RED la plataforma MQTT sigue funcionando al 100%.
- [ ] **NODERED-05**: Webhook no autenticado no dispara acciones.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
