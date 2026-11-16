# ADR: Single source of truth y propiedad

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Inventario único, muestras y RDF con proyecciones. Integraciones nunca duplican masters ni escriben tablas internas.

## Decisión
PostgreSQL master, Timescale series, RDF derivado; ERP autoridad transacciones comerciales; Node-RED flujos.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests outbox, duplicate update, partial failure, replay, consistency watermark y aislamiento.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
