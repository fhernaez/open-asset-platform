# ADR: Licenciamiento verificable

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
La distribución pública debe ser genuinamente FOSS, respetando terceros.

## Decisión
Inventario SPDX/SBOM, auditoría componente a componente, no copiar código propietario ni eliminar validaciones de licencia.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests dependency licenses policy, NOTICE, compliance checklist y cross-licensing.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
