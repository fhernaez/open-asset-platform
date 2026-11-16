# ADR: Bootstrap automático PostgreSQL

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Primera puesta Docker crea DB, extensión y migraciones sin operaciones manuales, volumen limpio o existente.

## Decisión
DB init standard + job db-bootstrap con credenciales administrativas scoped y script idempotente + migrator one-shot.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests docker up fresh, re-up, existing volume missing DB, missing extension fatal, concurrent boot.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
