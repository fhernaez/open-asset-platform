# ADR: MCP y asistente local desacoplados

Estado: **Propuesta aceptada para especificación**, su implementación queda pendiente de validación real.

## Contexto
Acceso a datos y configuración por agentes con autorización estricta y sin dependencia de LLM comercial.

## Decisión
Servidor MCP opcional con herramientas tipadas, OAuth/OIDC, guards; local model provider pluggable; write propose-confirm.

## Consecuencias
- Contratos públicos versionados; métricas y documentación deben evolucionar con código.
- Toda modificación incompatible exige nuevo ADR, migración/estrategia y cobertura de pruebas.
- No introducir excepciones de ingeniería por comodidad de implementación; registrar desviaciones.

## Alternativas consideradas
- Acoplamiento directo entre módulos o con runtime ajeno: rechazado por compatibilidad y soberanía del dato.
- Simplificar eliminando funciones: rechazado salvo priorización explícita de fases; el backlog de paridad sigue abierto.
- Implementación de alto riesgo sin pruebas: rechazada.

## Pruebas de decisión
Tests auth, tenant escalation, prompt injection, tool schema, replay, approval, disable.

## Referencias internas
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/quality/GATES.md`
- `docs/requirements/REQUIREMENTS.md`
