# Aceptación del plugin `ai_assistant` — G8

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **AI_ASSISTANT-01**: Prompt injection en documento no amplía scopes.
- [ ] **AI_ASSISTANT-02**: Usuario A no recupera embeddings/documentos de B.
- [ ] **AI_ASSISTANT-03**: LLM ausente no rompe API principal.
- [ ] **AI_ASSISTANT-04**: Aprobación requerida para escribir; acciones expiradas no ejecutan.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
