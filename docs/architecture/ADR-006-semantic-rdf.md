# ADR: IEC/ISO 81346 + Brick + Haystack

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Referencias técnicas representan función/producto/ubicación; relaciones semánticas extensibles, interoperables con vocabularios abiertos.

## Decisión
Identidad UUID estable; ontología oap, Brick/Haystack, RDF projection, SHACL; no reproducir textos de normas pagas.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests shape validation, round-trip RDF, URI stability, reference history y equivalencias.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
