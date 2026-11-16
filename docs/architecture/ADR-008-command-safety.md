# ADR: Seguridad de control físico

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Un bug o prompt malicioso no puede activar una instalación física de modo inadvertido.

## Decisión
CommandService central: role+object ACL, whitelist, validación límites, interlock, TTL, approvals, audit, fail-safe.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests denied commands, races, expiry, retries, offline, rollback and HIL mock before live.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
