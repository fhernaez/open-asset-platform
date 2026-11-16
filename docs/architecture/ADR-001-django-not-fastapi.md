# ADR: Framework Django como core, no FastAPI

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Modelos transaccionales, apps, migraciones, administración, GeoDjango y permisos ocupan el centro. FastAPI se excluye del core para unificar stack.

## Decisión
Django + DRF + GeoDjango y ASGI donde sea necesario; workers separados. No usar síncrono para loops IoT de alta frecuencia.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests de migrations, admin, DRF auth, GIS SRID, ASGI realtime y modularidad entre apps.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
