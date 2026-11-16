# `bacnet` — Escenarios Given/When/Then y evidencias

## Escenarios específicos obligatorios
### TEST-01 — Simulador BACnet discover/read temperatura; offline y retry.
**Given:** backend desplegado en Compose, plugin `bacnet` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-02 — Subs COV expiry/re-subscribe sin duplicar.
**Given:** backend desplegado en Compose, plugin `bacnet` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-03 — Reject write a property read-only y sin permissions.
**Given:** backend desplegado en Compose, plugin `bacnet` habilitado y fixture del contrato.
**When:** ejecutar entrada determinista vía API/UI/protocolo real, incluir intento usuario no autorizado.
**Then:** verificar efecto observable con query/response/log sanitizado; no usar mocks permanentes ni comprobar sólo que el endpoint devuelve 200. Registrar `docs/evidence/TEST_EVIDENCE_TEMPLATE.md`.

### TEST-04 — No discovery fuera de redes allowlisted.
**Given:** backend desplegado en Compose, plugin `bacnet` habilitado y fixture del contrato.
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
