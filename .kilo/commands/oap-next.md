# Avanzar historia siguiente
0. Consultar el grafo de conocimiento vigente (`graphify-out/graph.json`) para los módulos de la historia elegida: evita errores y ahorra tokens.
1. Consultar `docs/plan/BUILD_ORDER.md`, `docs/evidence/IMPLEMENTATION_STATUS.md`, `docs/requirements/TRACEABILITY.md`.
2. Elegir la primera historia no aceptada cuyas dependencias estén PASS y que tenga ejemplos/test definidos.
3. Delegar subagente según dominio, construir verticalmente (migración, backend, UI, tests) y revisar diffs.
4. Ejecutar quality gates, registrar evidencias e incidencias; no avanzar con regresiones.
5. Regenerar el grafo (`graphify extract /workspace/Open-Asset-Platform --code-only`) y commitearlo en el mismo commit del cambio.

## Reglas inamovibles de entrega
- El usuario despliega SOLO con Komodo (repo → Build → Deploy). Nunca dictarle comandos de terminal, builds manuales ni ediciones de archivos: todo cambio se aplica a `compose.yaml`/`compose.komodo.yaml` en el repo y las dependencias se resuelven dentro de los builds de los servicios.
- Sin operaciones irreversibles: nunca `docker compose down -v`, nunca migraciones destructivas; semillas idempotentes; versiones pineadas para rollback.
