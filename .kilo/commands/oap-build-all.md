# Construcción integral orquestada OAP — avanzar mientras gates PASS

**Objetivo:** una sola orden que inicia la construcción de todo el producto, sin saltar etapas ni ocultar bloqueos. Kilo opera durante la sesión de ejecución, no crea tareas en background por sí mismo.

1. Leer `AGENTS.md`, `CONTEXT.md`, `prompts/SYSTEM.md`, `docs/plan/BUILD_ORDER.md`, `docs/quality/GATES.md`, `docs/agents/ORCHESTRATION.md`.
2. Crear `.venv` como primera acción de código local: `python3 -m venv .venv`; verificar intérprete; no pip global.
3. Iniciar S00, ejecutar source/license audit cuando repos y herramientas accesibles; generar build tasks atómicas según plan.
4. Para cada historia y Sxx, delegar especialidades a subagentes, crear implementación funcional con migrations+API+UI+tests, ejecutar gates y registrar evidencia.
5. Si PASS, continuar a siguiente historia/hito dentro de los límites de la sesión. Si BLOCKED, detener cambios de nuevas etapas y producir informe con errores reproducibles y siguiente paso, sin prometer finalización posterior automática.
6. Las características no auditadas no se descartan: mantener traceability y `PARITY_*` como OPEN. Funciones comerciales no publicadas se implementan originalmente de acuerdo con requisitos, nunca mediante copia no autorizada.
7. Una entrega de software no se considera terminada hasta G9 verificado, incluidos tests Docker para DB volúmenes nuevo/existente, MQTT policies, plugins GUI restart y seguridad.
