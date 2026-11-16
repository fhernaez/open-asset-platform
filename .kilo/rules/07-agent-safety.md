# Agentes y MCP
- MCP y asistente se ejecutan con scopes/tenant del usuario, nunca acceso DB directo ni privilegios implícitos.
- Tools de lectura predeterminadas; escritura mediante propuesta-diff, permiso explícito, auditoría y idempotencia.
- No ejecutar acciones sobre equipos reales o cambios de infraestructura desde un prompt sin confirmación humana.
