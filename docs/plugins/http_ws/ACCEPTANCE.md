# Aceptación del plugin `http_ws` — G7

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **HTTP_WS-01**: HTTP 5xx reintento acotado con DLQ.
- [ ] **HTTP_WS-02**: SSRF contra localhost/metadata/reservadas bloqueado.
- [ ] **HTTP_WS-03**: Webhook con firma inválida o replay rechazado.
- [ ] **HTTP_WS-04**: Payload > máximo falla 413 y no se almacena.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
