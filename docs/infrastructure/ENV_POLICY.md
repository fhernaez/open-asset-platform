# Variables de entorno OAP — esquema, defaults, administración

## Archivo principal
`.env.example` es plantilla no secreta. `.env` local protegido por `.gitignore`; secretos en `secrets/*.txt` o mecanismo del runtime, nunca commitear. `PLUGIN_XXX_DEFAULT_ENABLED` se carga en instalación inicial, DESPUÉS GUI controla el valor persistente; `PLUGINS_BOOTSTRAP_MODE=once` no resetea a cada reboot.

## Grupos de configuración
1. `OAP_*` identidad, URL pública, logging, locale y time zone.
2. `DJANGO_*` hosts CSRF, secret path, env, workers.
3. `DB_*` host, port, app/db roles, passwords via files, extensiones, bootstrap.
4. `AUTH_*` bootstrap admin, OIDC, Keycloak opcional, scopes.
5. `MQTT_*` broker TLS ACL, ingress default, connection limits.
6. `TELEMETRY_*` retention, sampling defaults, quota max, late policy, buffering.
7. `SEMANTIC_*`, `SPATIAL_*` RDF/SHACL/map providers/local storage.
8. `PLUGINS_*` locks y seed mode; `PLUGIN_<NAME>_DEFAULT_ENABLED` para cada addon.
9. `NODERED_*`, `ERP_*`, `AI_*`, `MCP_*` solo defaults URLs/timeout sin credenciales planas.
10. `STORAGE_*`, `SMTP_*`, `OBSERVABILITY_*` archivos, notificaciones, traces.

## Variables y esquema validado
Cada clave tiene tipo, required, default, source, mutable, sensitive, enum/range. Fallar tempranamente si var mal escrita con prefijo reservado y si falta secreto obligatorio para plugin enabled. `DATABASE_URL` plana con password en Compose y logs es desaconsejada: preferir `_FILE` y secretos. Renderizar en UI sólo valores administrables no sensibles, con fuente/origen.

## Ejemplo importante
Primer boot `PLUGIN_MQTT_DEFAULT_ENABLED=true`; admin desactiva en GUI. Reiniciar container mantiene disabled (DB). Un hard lock en env gana; una instancia sin broker declara salud no disponible sin habilitar un loop de reconexión infinita.

## Requisitos críticos telemetría
`TELEMETRY_DEFAULT_STORAGE_MODE=on_change`, `TELEMETRY_DEFAULT_MAX_SAMPLES=...`, `TELEMETRY_DEFAULT_WINDOW=PT1H` son defaults para policy del MQTT Agent; cada atributo tiene override persistente, no reescribir sobre política ya configurada al restart.
