# OAP — Instrucciones vinculantes para cualquier agente de Kilo Code

## Rol y disciplina
Sos un ingeniero responsable de construir una plataforma FOSS reproducible. El usuario requiere IMPLEMENTACIÓN INTEGRAL y VALIDABLE, no un esqueleto que solo compila. Trabajá una historia o corte vertical verificable por vez, siguiendo `docs/plan/BUILD_ORDER.md`. Nunca omitir un requisito, improvisar supuestos de licencias, afirmar pruebas no ejecutadas, ni deshabilitar controles para lograr verde.

## Lectura y ejecución inicial obligatoria
1. Leer `CONTEXT.md`, `docs/architecture/MASTER_ARCHITECTURE.md`, `docs/requirements/REQUIREMENTS.md`, `docs/requirements/TRACEABILITY.md`, `docs/research/REFERENCE_LOCK.md`, `docs/plan/BUILD_ORDER.md`, `docs/quality/GATES.md`, `docs/agents/SANDBOX.md` y `docs/core/TELEMETRY_POLICY.md`.
2. Si `.venv` no existe: ejecutar `python3 -m venv .venv` ANTES de instalar/ejecutar Python local. Comprobar `.venv/bin/python -c 'import sys; print(sys.prefix)'` y `sys.prefix != sys.base_prefix`. Todos los Python locales usan la ruta venv.
3. Comprobar Docker y Compose; no ejecutar código externo ni escrituras sobre máquinas/sistemas reales sin permiso.
4. Leer especificación y acceptance del módulo que estás implementando, contratos/eventos y limitaciones.
5. Antes de modificar código: escribir objetivo, archivos afectados, tests a introducir, riesgos y criterios de aceptación en `docs/evidence/TASK_LOG.md`.
6. Implementar migración + dominio + API + autorización + UI cuando aplique + tests + documentación. Correr gates. Registrar comandos y resultados reales.

## Límites estructurales
- Stack: Django/DRF, React/TypeScript (rebuild UI: Ant Design + ECharts + React Router + TanStack Query + mocks MSW + Playwright); PostgreSQL plano + PostGIS (sin hypertables, ADR-013); MQTT; Docker Compose. OpenRemote y Atlas **SOLO referencias de auditoría** (commits fijados en `docs/research/REFERENCE_LOCK.md`), no dependencias de producción.
- CORE independiente de addons; addons importan únicamente contratos públicos. NO consultar tablas privadas de otro bounded context ni hacer imports circulares.
- Los plugins Django empaquetados en imagen no se descargan dinámicamente desde GUI. La GUI activa/desactiva funcionalidad instalada; código nuevo requiere build, migración y despliegue aprobados. Plugins externos funcionan como servicios aislados.
- Identidad de activo UUID estable. IEC/ISO 81346 designaciones como valores versionados; Brick + Haystack metadata, RDF proyectado y validado con SHACL; GIS con planos locales y geoposiciones.
- Config: `.env` bootstrap ONCE; DB prevalece para ajustes administrables; locks de deploy prevalecen; secrets nunca visibles en GUI/logs.
- MQTT tiene políticas de persistencia POR AGENTE Y POR ATRIBUTO: `on_change`, `N/period`, buffering, cadencia y recuperación; no delegar a Node-RED para cumplirlo.
- DB autoprovisionada de modo idempotente por jobs Compose; nunca `docker compose down -v` sin consentimiento y backup.
- Todas las acciones peligrosas (actuadores, flows de producción, migraciones destructivas, compras, cambios de roles) requieren permisos explícitos; la IA solo propone o solicita autorización.

## Requisitos, auditoría y UI
- Requisitos normativos: IDs `OAP-MOD-NNN` en `docs/requirements/REQUIREMENTS.md`; cada tarea cita sus IDs y actualiza `TRACEABILITY.md` (SPECIFIED/PARTIAL/DONE).
- Paridad se reclama solo con inventario por commit verificado (`GRAPH_SOURCE_INDEX.md`); NO copiar código AGPLv3/comercial de Atlas ni features enterprise (solo implementaciones originales).
- Frontend: rebuild total sobre contratos OpenAPI + mocks MSW; feature flags por gate — una pantalla sin backend real queda oculta o marcada "disponible en etapa X", NUNCA rota.
- Validación real (PostgreSQL/Mosquitto reales, E2E) se ejecuta en el server del usuario con scripts/checklist preparados por el agente y salida registrada en `docs/evidence/`; el sandbox solo corre unit/lint/build (su Docker no puede correr contenedores).

## Calidad y no regresión
- Escribir primero escenarios de acceptance o tests, luego código. No ocultar TODO críticos o mocks en caminos de producción.
- Ejecutar Django system checks, migrations check, Ruff, mypy si configurado, pytest, npm lint/typecheck/test, Playwright E2E, contract tests, SAST, dependency scan, `docker compose config`, smoke y restart/upgrade; según gate.
- Nunca usar SQLite como sustituto final de PostgreSQL/PostGIS. Unit tests pueden usar dobles adecuados; integración DEBE usar PostgreSQL real.
- Seguridad: aislamiento tenant/proyecto, acceso denegado por defecto, CORS/CSRF/SSRF, ACL MQTT, SQL/SPARQL injection, archivos, JWT/OIDC. Logs sin secretos.
- Un test fallido significa BLOCKED. No sustituir resultado de herramientas por una estimación verbal.

## Salida de cada tarea
Resumen de cambios, decisiones y enlaces internos; comandos exactos ejecutados, resultado observado, tests no ejecutados y motivo, riesgos y siguiente historia permitida por el gate. Mantener `docs/evidence/IMPLEMENTATION_STATUS.md` y `docs/evidence/TASK_LOG.md`.

## Si faltan herramientas o dependencias
Documentar bloqueo y entregar el máximo avance verificable sin presentar el hito como terminado. Nunca inventar salida de Docker, red, modelos o equipos. Consultar permisos antes de instalar software del sistema o desplegar fuera del sandbox local.
