# ADR: SpatialScene multiproyecto

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Planos e imágenes y GIS geográfico en urbano/rural/industrial/edificios; no forzar lat/lon a píxeles.

## Decisión
Scene, Layer, Placement, local/geo CRS, transformación, MapLibre y proveedor de mapas opt-in.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests 2+ capas, zoom/resize, SRID correcto, georref, roles en assets y offline.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
