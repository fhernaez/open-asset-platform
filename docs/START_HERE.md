# Guía de arranque en Kilo Code

1. Extraer ZIP **sin carpeta extra intermedia** en directorio de proyecto vacío; ver `AGENTS.md`, `CONTEXT.md`, `kilo.jsonc`, `.kilo/`, `docs/` directamente en la raíz.
2. Crear `.venv`: `python3 -m venv .venv`; confirmar `.venv/bin/python -c 'import sys; assert sys.prefix != sys.base_prefix'`.
3. Comprobar especificaciones con `.venv/bin/python scripts/check_spec_kit.py` y leer reporte.
4. Abrir Kilo Code, seleccionar modelo local/remoto que ya uses. Seleccionar agente `oap-lead`, o Code si no aparece. No usar otro sistema de prompts sin leer `prompts/SYSTEM.md`.
5. Ejecutar `/oap-build-all` si querés que avance por etapas y se detenga en bloqueos, o `/oap-start` y luego `/oap-next` para revisar manualmente cada hito.
6. Para cada historia, exigir tests reproducibles y evidencia: `docs/evidence/IMPLEMENTATION_STATUS.md` y `TASK_LOG.md`.
7. Ejecutar `/oap-validate` antes de dar por funcional cada fase; `bash scripts/quality_gate.sh G4` falla al inicio del kit porque falta el producto, lo cual es CORRECTO.

**Si Kilo no reconoce los comandos:** abrir y pegar el contenido de `.kilo/commands/oap-build-all.md` en chat. Las rutas de reglas y agentes de Kilo corresponden a la documentación consultada en noviembre de 2026; versiones del plugin/CLI podrían cambiar.

**Distinguir hitos:** kit de especificación validado ≠ app funcional. Un LLM puede equivocarse; gates son esenciales, pero la seguridad operacional final requiere ensayos con equipos, revisión de licencias y aceptación por responsables humanos.
