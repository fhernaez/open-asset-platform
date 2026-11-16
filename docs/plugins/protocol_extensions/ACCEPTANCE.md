# Aceptación del plugin `protocol_extensions` — G9

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **PROTOCOL_EXTENSIONS-01**: Driver disabled no accede red.
- [ ] **PROTOCOL_EXTENSIONS-02**: Contrato de datos consistente entre MQTT/Modbus/BACnet/OPC UA.
- [ ] **PROTOCOL_EXTENSIONS-03**: Credenciales de protocolos aisladas y no visibles en export.
- [ ] **PROTOCOL_EXTENSIONS-04**: Pruebas simulador por protocolo, no stub.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
