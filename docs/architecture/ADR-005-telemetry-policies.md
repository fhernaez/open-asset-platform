# ADR: Almacenamiento MQTT selectivo

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
La aplicación debe permitir no saturar storage: cambios y cuota muestras por período en MQTT agent/atributo sin Node-RED.

## Decisión
Ingesta current first; después filtro StoragePolicy on_change/maxN/window; override agente/atributo, jitter y políticas reconfigurables.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests diferencia analógico/digital, 1000 duplicados, N/T, restart, bursts, null/NaN, alarmas independientes.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
