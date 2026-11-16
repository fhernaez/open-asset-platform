# Plugin `mcp_server` — especificación funcional y técnica

**Gate de aceptación:** G8. **Estado inicial:** diseño; no está implementado. No presentar stub como un plugin completo.

## Problema y capacidades
Servidor MCP de herramientas, recursos y prompts documentados para agentes externos y el asistente local, usando authz del dominio OAP.

## Dependencias (contratos públicos; no imports privados)
- `identity`
- `assets`
- `semantics`
- `events`

## Modelo propio de dominio / tablas (borrador a formalizar migrando)
- `McpToolDefinition(name,version,json_schema,scope,side_effect)`
- `McpGrant(principal,project,tools,expires)`
- `McpInvocation(actor,tool,input_hash,result_status,trace)`
- `McpApproval(proposal,approver,expiry)`

## Historias de usuario y workflows de extremo a extremo
1. Publicar tools lectura assets.search/get_graph, scenes.get, telemetry.query bounded y semantic.validate, limits.
2. Exponer tools de escritura inicialmente solo `propose_*`; confirmar produce cambio mediante servicios DRF con auditoría.
3. Aceptar sólo transporte recomendado por SDK vigente y validar tokens issuer/audience/scope TLS; no exponer creds LLM.
4. Deshabilitar plugin inmediatamente bloquea nuevas invocaciones y mantiene auditoría.

## Interfaz HTTP — endpoints a especificar en OpenAPI v1
- `/mcp (Streamable HTTP, según SDK vigente)` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mcp/tools` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mcp/grants` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.
- `/api/v1/mcp/invocations` — ACL por tenant/proyecto, schema validado, paginación/idempotencia cuando proceda.

## Interfaz React / criterios UX
- Administrador roles/tool grants y auditoría
- Vista aprobar/rechazar propuesta y mostrar diff de asset/flow

## Eventos, permisos y estado
- Definir `events` emitidos/consumidos en `docs/contracts/EVENT_CATALOG.md`; publicar por outbox sólo tras DB commit.
- Plugin declara `required_capabilities`, dependencia de otros plugins y `PluginSetting` JSON Schema. Activación por scope validada y auditada; desactivación limpia timers/suscripciones sin perder datos.
- Todos los endpoints requieren autenticación y permisos de objeto, además del rol de gestión para configuraciones; no acceso directo a secretos ni tablas de terceros.
- Errores uniformes: 400 validación superficial, 401 sin autenticar, 403 prohibido, 404 fuera de scope, 409 conflicto/version, 422 regla semántica, 503 dependencia externa caída; documentar el uso exacto.
- Los servicios externos utilizan retries con backoff, timeouts, idempotencia, health/readiness, telemetry de fallos y DLQ cuando aplica.

## Configuración ambiental (solo defaults y parámetros de despliegue)
- `PLUGIN_MCP_DEFAULT_ENABLED`
- `MCP_PUBLIC_URL`
- `MCP_REQUIRE_AUTH`
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
