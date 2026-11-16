# ADR: ERP y Node-RED como externos

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
No replicar ERP contable. Node-RED opcional de integración, nunca ingest path obligatorio.

## Decisión
Conectores con event outbox/webhook/MQTT, mapeos import/export flows versionados sin secretos.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests divergence, idempotent, secret exclusion, ERP callback auth, fail retries.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
