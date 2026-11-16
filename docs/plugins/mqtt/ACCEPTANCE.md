# Aceptación del plugin `mqtt` — G4

Los siguientes escenarios son bloqueantes. Kilo debe convertirlos en pytest (unit/integration), contract tests y Playwright E2E cuando incluyan GUI. Guardar fixture, comando y salida observada en evidencia.

- [ ] **MQTT-01**: 1000 payloads mismos valores -> 1 fila TSDB, 1000 current/rule observations y counters correctos.
- [ ] **MQTT-02**: Cambios 1,2,2,3 -> 3 filas si no aplica cap.
- [ ] **MQTT-03**: Agent N=2, Attribute N=5 -> 2 y 5 respectivamente en misma ventana, persistente al reinicio.
- [ ] **MQTT-04**: Dos workers compiten por cuota N=3 -> nunca 4 puntos.
- [ ] **MQTT-05**: Reconnect + QoS1 replay -> no duplicated history; 403 publish sin permiso.
- [ ] **MQTT-06**: Ningún servicio Node-RED levantado y MQTT sigue funcionando.

## Negativos obligatorios
- [ ] Tenant B no puede consultar/modificar dato de A incluso si conoce UUID.
- [ ] Plugin deshabilitado rechaza nuevas operaciones y no daña otros plugins.
- [ ] Servicio externo caído deja estado visible y retries acotados, no bloquea Django.
- [ ] Config inválida no se guarda, secret no sale por API/log.
- [ ] API/UI rechaza payload inválido con error estable sin stacktrace.

## Evidencia requerida
Reportar ID de test, código ejercitado, BD/broker/simulador real usado, commands, logs sanitizados, capturas GUI si aplica, estado PASS/BLOCKED, defectos abiertos y revisión QA independiente. La inexistencia de test equivale a BLOCKED.
