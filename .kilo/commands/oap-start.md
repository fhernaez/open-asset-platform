# Inicio orquestado de OAP
1. Leer `AGENTS.md`, `CONTEXT.md`, `prompts/SYSTEM.md` y `docs/agents/ORCHESTRATION.md`; confirmar estructura en raíz.
2. Ejecutar `python3 scripts/check_spec_kit.py` (único Python permitido antes de `.venv` para verificar kit? preferentemente crear venv primero) y crear **primero** `.venv` con `python3 -m venv .venv`. En adelante `.venv/bin/python scripts/check_spec_kit.py`.
3. Verificar disponibilidad Docker Compose/Node y versionar dependencias. No modificar host con sudo.
4. Revisar estado `docs/evidence/IMPLEMENTATION_STATUS.md`, source audit y licencias. Identificar primer gate bloqueante.
5. Escribir plan inmediato de máximo un hito, delegar tareas a subagentes por contrato y ejecutar `docs/plan/BUILD_ORDER.md`, sin generar decenas de archivos placeholder.
6. Tras cambios, ejecutar gates y documentar evidencia. No declarar sistema funcional si solo está scaffolded.
