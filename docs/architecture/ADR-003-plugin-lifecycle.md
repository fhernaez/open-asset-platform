# ADR: Módulos estables y addons administrables

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Django Apps se registran al arranque. Instalar paquetes nuevos en caliente con migraciones es inseguro y no soportado.

## Decisión
Separar installed/enabled/configured/healthy; defaults env seed-once y cambios DB; external services cuando haga falta aislamiento.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests plugin enable/disable, restart, conflicts, perms, dependency cycles, migration compatibility.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
