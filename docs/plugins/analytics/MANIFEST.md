# Plugin manifest — `analytics`

## Declaración de extensión a construir
```yaml
id: oap.analytics
version: 0.1.0
core_api: '>=1.0,<2.0'
kind: django_app  # cambiar a isolated_service si procede
requires: ["telemetry", "cmms", "assets", "dashboards"]
activation_scope: [platform, tenant, project]
admin_toggle: true
install_requires_redeploy: true
healthcheck: required
migrations: forward_compatible
configuration_schema: required
ui_extension_manifest: required
```
`MANIFEST.md` es especificación, no YAML final cargable. Kilo genera `plugin.yaml` y su JSON Schema al implementar, con análisis de dependencias y licences. No todo `requires` es plugin: referencias a core services no son activables.

## Ciclo de vida
`AVAILABLE -> INSTALLED -> CONFIGURED -> ENABLED -> DISABLING -> DISABLED`, errores `UNAVAILABLE`, `INCOMPATIBLE`, `RESTART_REQUIRED`, `FAILED`.

## Versión, datos y garantías
Deshabilitar no elimina datos/migraciones. Instalar versión nueva necesita image deploy y migración controlada. Cambiar `DEFAULT_ENABLED` en `.env` no pisa activaciones existentes; un locked disabled sí impide habilitar. Eventos y endpoints versionados; contract tests en CI.
