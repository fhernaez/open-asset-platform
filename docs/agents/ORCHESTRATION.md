# Manual de orquestación Kilo Code: agentes, tareas y checkpoints

## Modelo de responsabilidad
El agente líder `oap-lead` es único responsable de integrar los cambios y del estado G0-G9. Cada subagente trabaja sobre una historia y recibe el mínimo contexto necesario: contrato público, dominio, fixture, acceptance, owner de la BD, archivos permitidos y recursos de prueba. Los LLM de Kilo son seleccionados por el usuario; no se exigen credenciales nuevas.

## Protocolo de delegación
1. Líder inspecciona `docs/evidence/IMPLEMENTATION_STATUS.md`, identifica próxima historia con dependencias PASS y redacta brief con IDs, entrada, salida, rutas y test.
2. Auditor verifica diseño antes de paralelizar. Backend y frontend pueden paralelizar si OpenAPI/JSON Schema ya fue aprobado; devops e IoT pueden avanzar con contrato de evento congelado.
3. Cada subagente guarda cambios aislados, sin reescribir áreas de otros; comunica archivos tocados y conflictos antes del merge.
4. `quality-security` efectúa revisión independiente, intenta romper tenant isolation y condiciones MQTT, y entrega lista de bloqueantes.
5. Líder integra, corre unit/integration/E2E, actualiza `docs/evidence/TASK_LOG.md` y `IMPLEMENTATION_STATUS.md` con comando/exit code/log.
6. Sólo el líder puede declarar gate PASS; ningún subagente aprueba sus propias pruebas como única evidencia.

## Campos obligatorios del task brief
`story_id`, `requirement_ids`, `goal`, `preconditions`, `files_allowed`, `contract_version`, `test_fixtures`, `negative_cases`, `security_context`, `definition_of_done`, `do_not_touch`, `report_to`.

## Política de interrupción/reanudación
No asumir que Kilo reanuda automáticamente tras reiniciar. Escribir un checkpoint explícito: último commit/archivos, gate, resultados reproducibles, pendientes, siguiente comando y riesgos. El siguiente agente leerá los archivos, no memoria del chat. Nunca usar resultados no guardados como única fuente.

## Métricas de trabajo
Tiempo de tests y build, cantidad de requisitos cerrados con evidencia, conflictos de dependencias, migraciones compatibles, vulnerabilidades, cobertura crítica y regresiones. Velocidad de generación de código NO mide funcionalidad.
