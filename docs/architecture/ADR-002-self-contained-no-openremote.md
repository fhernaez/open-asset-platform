# ADR: Producto independiente

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
OpenRemote y Atlas son referencias de prestaciones y auditoría de código/licencias, no servicios ejecutándose en paralelo.

## Decisión
Crear adapters de dispositivos, reglas, dashboards, usuarios, Edge y módulos CMMS nativos. Fijar commits de referencia y medir paridad por capability.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Compose jamás depende de openremote/atlas; buscar referencias a sus APIs en runtime y bloquear; reportes de features y tests.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
