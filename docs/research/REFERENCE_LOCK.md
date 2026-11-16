# Baselines de repositorios y estándares — fijar antes de implementar paridad

- `https://github.com/openremote/core` — referencia funcional, no dependencia runtime; seleccionar commit/tag concreto, obtener hash, árbol y licencia.
- `https://github.com/Grashjs/cmms` — referencia funcional, no dependencia runtime; seleccionar commit/tag concreto, hashes subproyectos, license NOTICE.
- `https://kilo.ai/docs/customize/agents-md`, `.../custom-rules`, `.../workflows`, `.../custom-modes`: rutas Kilo documentadas a noviembre 2026.
- `https://docs.djangoproject.com/en/5.2/` — documentación Django 5.2 LTS; antes de instalar confirmar versiones soportadas y fijar en lock.
- `https://docs.docker.com/guides/postgresql/` — init scripts solo con directorio de datos vacío.
- `https://docs.docker.com/compose/how-tos/startup-order/` — service_healthy y service_completed_successfully.
- `https://docs.brickschema.org/`, `https://www.project-haystack.org/`, IEC/ISO 81346 (norma con copyright, obtener legítimamente), GeoSPARQL, SHACL, W3C RDF.

## Registro obligatorio
`name | remote_url | sha256/commit | date_utc | license_spdx | paths_audited | api_refs | doc_refs | reviewed_by`. Dejar sin completar donde no exista evidencia, nunca inventar hash.

## Advertencia funcional
Las limitaciones de OpenRemote sobre on-change y límite N/T son **observaciones de uso planteadas por el usuario** que OAP DEBE resolver; no tratarlas como conclusión definitiva sobre todas las versiones de OpenRemote sin inspección específica.
