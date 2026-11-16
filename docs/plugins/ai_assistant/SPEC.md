# Plugin `ai_assistant` — especificación funcional y técnica

**Gate de aceptación:** G8. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Asistente local opcional basado en LLM configurable (Ollama, llama.cpp o API compatible), consulta semántica, ayuda de onboarding e inferencia con evidencia.

## Dependencias (contratos públicos; no imports privados)
- `identity`
- `assets`
- `semantics`
- `mcp_server`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `ModelProvider(endpoint,model_id,secret_ref,local_only)`
- `AssistantSession(user,project,history_policy)`
- `AssistantToolGrant(tool,role,write_approval)`
- `DocumentIndex(source_id,chunk_hash,embedding_model)`
- `AssistantRun(trace,token_usage,tool_calls,approval_state)`

## Historias de usuario y workflows de extremo a extremo
1. Usuario consulta activos y fallas; RAG restringido por tenant+project sobre documentos y RDF; citar source ids sin inventar.
2. Asistente genera propuesta SHACL/IEC/Node-RED/maintenance con preview diff, nunca modifica directo.
3. Si solicita acción write, emite MCP/tool proposal, verifica RBAC y aprobación humana, graba audit.
4. Sin motor LLM activo, core y plugins restantes continúan y GUI muestra servicio no disponible.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/api/v1/assistant/chat` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/assistant/sessions` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/assistant/proposals/{id}:approve` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/assistant/models` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Panel chat contextual en activo/proyecto y citas/acciones revisables
- Selector modelo local y herramientas autorizadas por rol

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_AI_DEFAULT_ENABLED`
- `AI_PROVIDER`
- `AI_BASE_URL`
- `AI_MODEL`
Los defaults se importan ONCE a PostgreSQL; las preferencias administrables se editan en GUI y persisten al reinicio. Secret references no exponen credenciales. Los flags locked de deploy prevalecen.

## Riesgos específicos
- Una integración puede estar ausente, lenta o mal configurada: el CORE debe mantenerse operativo.
- Cambios de contrato requieren versionado, migraciones compatibles y regresión E2E; no modificar definiciones de activos ajenas.
- Para controles físicos aplicar `CommandService`, aprobación y tests en simulador; no ejecutar hardware real como parte del CI.
- Una capacidad listada no se considera implementada sin pruebas que ejerciten su efecto observable en base real/UI.

## Documentos vinculados
- `docs/architecture/MASTER_ARCHITECTURE.md`
- `docs/contracts/PLUGIN_CONTRACT.md`, `docs/contracts/EVENT_CATALOG.md`, `docs/quality/GATES.md`
- `{base}/ACCEPTANCE.md`
