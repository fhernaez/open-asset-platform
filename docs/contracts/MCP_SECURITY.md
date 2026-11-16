# API MCP — permisos y aprobación

## Capas
Servidor MCP aislado en Docker, autenticación OAuth/OIDC de recursos y transporte HTTP conforme al SDK fijado; no aceptar llamadas anónimas si no es configuración de laboratorio explícita. Tools/resources/prompts se registran versionados y se despublican al deshabilitar plugin.

## Herramientas v1
- Lectura: `projects.list`, `assets.search`, `assets.get`, `assets.get_graph`, `spatial.get_scene`, `telemetry.get_current`, `telemetry.query_history`, `cmms.list_orders`, `semantic.validate`.
- Propuesta: `assets.propose_update`, `nodered.preview_flow`, `cmms.propose_work_order`, `config.propose_plugin_toggle`.
- Commit: `proposals.confirm` solamente con approval grant separado, actor autorizado, TTL, check revision, idempotency key, audit. No permitir `set_actuator` directa.

## Scopes
Scoping `tenant/project/resource` obligatorio, rate limits, output size limits. No leer secrets/settings privados ni documentos fuera del tenant. Cada tool delega en `AuthzService` + `DomainService`, jamás ORM directo. Prompt injection en recursos/documents se trata como datos no confiables.

## Tests
Token expirado, otra audiencia, scope insuficiente, tenant B, proposal replay, aprobación por autor no autorizado, instrucción adversarial y MCP disabled. Responder error controlado sin datos sensibles.
