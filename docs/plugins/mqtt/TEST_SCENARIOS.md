# `mqtt` — Escenarios Given/When/Then y evidencias

## Escenarios específicos obligatorios
### TEST-01 — 1000 payloads mismos valores -> 1 fila TSDB, 1000 current/rule observations y counters correctos.
**Given:** backend desplegado en Compose, plugin `mqtt` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-02 — Cambios 1,2,2,3 -> 3 filas si no aplica cap.
**Given:** backend desplegado en Compose, plugin `mqtt` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-03 — Agent N=2, Attribute N=5 -> 2 y 5 respectivamente en misma ventana, persistente al reinicio.
**Given:** backend desplegado en Compose, plugin `mqtt` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-04 — Dos workers compiten por cuota N=3 -> nunca 4 puntos.
**Given:** backend desplegado en Compose, plugin `mqtt` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-05 — Reconnect + QoS1 replay -> no duplicated history; 403 publish sin permiso.
**Given:** backend desplegado en Compose, plugin `mqtt` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-06 — Ningún servicio Node-RED levantado y MQTT sigue funcionando.
**Given:** backend desplegado en Compose, plugin `mqtt` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.


## Suite común no negociable
- Arranque con plugin instalado-disabled, llamada API rechazada, base funcional intacta.
- Enable/disable por GUI con permiso y cambio registrado; restart conserva preferencia, locked disabled vence override.
- Acceso tenant B con UUID A es denegado, no hay datos en logs ni respuesta.
- Migración plugin y downgrade compatible no altera historia ni configuración.
- Eventos duplicados/retry no provocan operaciones duplicadas; salud del worker es observable.
- Una falla de integración no bloquea resto de la plataforma ni provoca CPU/retries sin límites.

## Evidencia gate
Registrar test exacto/pytest o Playwright file, fixture, comando, exit code, SQL si cuenta filas, captura de UI si aplica y QA reviewer. Tests no ejecutados = BLOCKED. No correr dispositivos físicos desde CI.
