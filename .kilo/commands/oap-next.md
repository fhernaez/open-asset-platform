# Avanzar historia siguiente
1. Consultar `docs/plan/BUILD_ORDER.md`, `docs/evidence/IMPLEMENTATION_STATUS.md`, `docs/requirements/TRACEABILITY.md`.
2. Elegir la primera historia no aceptada cuyas dependencias estén PASS y que tenga ejemplos/test definidos.
3. Delegar subagente según dominio, construir verticalmente (migración, backend, UI, tests) y revisar diffs.
4. Ejecutar quality gates, registrar evidencias e incidencias; no avanzar con regresiones.
