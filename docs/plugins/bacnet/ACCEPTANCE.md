# Aceptación del plugin `bacnet` — G7

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **BACNET-01**: Simulador BACnet discover/read temperatura; offline y retry.
- [ ] **BACNET-02**: Subs COV expiry/re-subscribe sin duplicar.
- [ ] **BACNET-03**: Reject write a property read-only y sin permissions.
- [ ] **BACNET-04**: No discovery fuera de redes allowlisted.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
