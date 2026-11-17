# OAP — Open Asset Platform | Especificación integral para Kilo Code

**Este repositorio inicial es un PLAN DE CONSTRUCCIÓN EJECUTABLE POR AGENTES, no una aplicación terminada.**
Version del contrato: `SPEC-1.0`; idioma de la documentación: español. Código y APIs en inglés. Los agentes deben trabajar incrementalmente, ejecutar pruebas y dejar evidencia; nunca afirmar paridad antes de comprobarla.

## Resultado buscado
Plataforma autohospedada, distribuible como Docker, independiente de OpenRemote y Atlas en tiempo de ejecución. Nuevo backend **Django/DRF + GeoDjango**, frontend **React/TypeScript**, **PostgreSQL + PostGIS**, broker MQTT, workers y addons activables desde administración. Reimplementar por especificación las capacidades de referencia OpenRemote y Atlas CMMS; no retirar ni puentear restricciones de licencias ajenas: implementar capacidades originales y cumplir licencias FOSS. Multitenancy, motor de reglas, BMS/EMS, CMMS, RDF/SHACL, IEC/ISO 81346 + Brick + Haystack, GIS/planos, Node-RED bidireccional opcional, ERP externo, asistente local y servidor MCP.

## Primer uso: NO comenzar creando 100 módulos vacíos
1. Extraer el contenido **en la raíz** del workspace, asegurando `AGENTS.md`, `CONTEXT.md`, `kilo.jsonc` y `.kilo/` en raíz.
2. Ejecutar `python3 scripts/check_spec_kit.py` (verifica DOCUMENTOS, no prueba la aplicación).
3. Iniciar Kilo Code y seleccionar **`oap-lead`** si el cliente lo detecta; en alternativa, agente Code con el prompt `prompts/SYSTEM.md` y contexto `prompts/CONTEXT.md`. La configuración de modelos la controla el usuario en Kilo: NO hardcodear proveedores.
4. Iniciar **`/oap-start`** (ver `.kilo/commands/oap-start.md`). Las reglas cargadas por Kilo hacen respetar contratos, sandbox y política de no avanzar con gates fallidos.
5. La PRIMERA acción de código es crear `.venv` con `python3 -m venv .venv`. Todos los comandos Python locales deberán usar `.venv/bin/python`, `.venv/bin/pip`, `.venv/bin/pytest`, etc. Nunca instalar en Python global. Windows: `.venv/Scripts/python.exe`.
6. Implementar los hitos de `docs/plan/BUILD_ORDER.md`. Primer hito usable: Docker PostgreSQL inicializable automáticamente + Django health + login + activos + plugin toggles + MQTT change-aware + vista simple, con pruebas reales.
7. Registrar progreso y evidencia en `docs/evidence/IMPLEMENTATION_STATUS.md`, no sustituir pruebas con texto plausible.

## Navegación obligatoria
- `AGENTS.md`, `CONTEXT.md`, `.kilo/rules/`: reglas que se leen en cada tarea.
- `docs/architecture/MASTER_ARCHITECTURE.md` y ADR: arquitectura, topología y decisiones.
- `docs/requirements/REQUIREMENTS.md`, `docs/requirements/PARITY_*.md`: requisitos completos y paridad trazable.
- `docs/core/`: especificación detallada por bounded context del CORE.
- `docs/plugins/<addon>/`: especificación, modelo, API, UI, acceptance y despliegue por plugin.
- `docs/infrastructure/`: Docker, bootstrap PostgreSQL, .venv, secretos, variables, pruebas de restore.
- `docs/quality/`: pirámide de pruebas, gates y casos detallados.
- `docs/agents/`: ciclo de delegación, prompts por especialidad y sandbox.
- `docs/plan/`: secuencia y dependencias de construcción, criterios de finalización.

## Requisitos críticos explícitos
- **MQTT**: soporte nativo de ingesta sin Node-RED; en `MQTT Agent` y en cada atributo con `storageDatapoint=true`, seleccionar `on_change` (solo persistir cuando cambia), configurar tolerancia y definir máximo **N muestras por ventana T** y/o cadencia de muestra uniforme. Las reglas procesan valores recibidos aun cuando no se almacenen. Probar ráfagas, retención, límites y deduplicación. `docs/core/TELEMETRY_POLICY.md` es el contrato normativo.
- **BASE DE DATOS**: el primer `docker compose up` crea automáticamente BD, roles/esquemas/extensiones y aplica migraciones, de forma idempotente, incluso si hay volumen preexistente sin la DB de aplicación. `docs/infrastructure/DB_BOOTSTRAP.md`.
- **.venv**: obligatorio antes de cualquier instalación o comando Python local; excluirlo de Git y del ZIP de fuente. Ambiente Docker usa dependencias de imagen reproducibles y no instala paquetes globales en la máquina anfitriona.
- **Fuente única de verdad**: identidad de activo y permisos centralizados, RDF como proyección, no sincronización de inventarios masters entre OpenRemote/Atlas/Node-RED.

## Limitaciones de este kit
Los repositorios de referencia aún requieren auditoría por commits fijados, análisis de código y matriz de diferencias. El material actual especifica la meta y las pruebas, no acredita paridad completa. Los servicios de producción dependen de credenciales, equipos y pruebas del operador. No usar soluciones que comprometan seguridad operacional.

## Licencias y atribución
`docs/legal/LICENSING_AND_CLEAN_ROOM.md`. No eliminar validación de licencias ni copiar código cerrado. La decisión final de licencia de OAP debe ser compatible con cualquier código reutilizado; no usar marcas originales de terceros como propia.
