# Contrato de configuración ENV / DB / GUI

## Niveles y precedencia
- **Despliegue obligatorio** (no editable GUI): `APP_ENV`, public URL/allowed hosts/TLS, DB connectivity, secrets, OIDC issuers, MQTT network, resource limits.
- **Locks de seguridad** (env): `PLUGIN_LOCKED_DISABLED`, `FEATURE_PHYSICAL_COMMANDS_LOCKED`, `MCP_WRITE_LOCKED`. Nunca anulables por DB.
- **Bootstrap defaults**: `PLUGIN_<KEY>_DEFAULT_ENABLED`, `APP_DEFAULT_LOCALE`, otras defaults. `BOOTSTRAP_CONFIG_MODE=once`: crear missing definitions/activations, pero NO pisar overrides.
- **Overrides administrables** (DB): activaciones, sampling, alarm thresholds, dashboards, integraciones opt-in, default models y proyecto.
- **Code defaults**: fallback validado y documentado para entornos nuevos.

## Precedencia efectiva por clave
`deployment-lock` > `db scoped override (project → tenant → platform)` > `initial seed` > `code default`; keys solo-deploy no aceptan override. El “locked disabled” aplica siempre: `effective_enabled = installed && enabled_global && enabled_tenant && enabled_project && deps_ok && !locked_disabled && healthy_preconditions`. Health no implica que se borre la preferencia enabled.

## Entidades de auditoría
`ConfigDefinition(key, type, scope, default, mutable, needs_restart, secret, validation_schema)`, `ConfigOverride(key, scope, value, revision)`, `ConfigChange(actor, before_hash, after_hash, trace)`. ETag versionado para concurrent writes. `SecretReference` apunta a Docker secrets/vault; nunca almacenar contraseñas en JSON settings.

## Validación y UI
El plugin declara JSON Schema incluyendo min/max/enum/ui-hints; API valida y presenta mensaje legible. Cada control muestra `currentValue`, `effectiveSource`, `locked`, `restartRequired`, `modifiedBy`, `modifiedAt` y restauración al default. Las claves desconocidas generan error en entorno estricto (no ignorarlas silenciosamente). Migrar nombres de variables deprecated con warnings y tests.

## Ejemplo
`.env: PLUGIN_CMMS_DEFAULT_ENABLED=false` → bootstrap DB cmms.enabled=false. El admin cambia cmms.enabled=true. Restart con misma env mantiene true. Cambio de `.env` a `PLUGIN_CMMS_DEFAULT_ENABLED=false` no sobreescribe. `PLUGIN_LOCKED_DISABLED=cmms` deshabilita efectivamente, UI muestra bloqueo y override true persiste pero no se aplica. Al quitar lock, regresa el override anterior después de verificación de dependencias.

## Resiliencia
Si PostgreSQL está caído, no cargar config incorrecta desde env silenciosamente y abrir acceso. Modo degradado seguro/read-only según políticas; actuar fail-closed para plugins comandos físicos, MCP writes e integraciones.
