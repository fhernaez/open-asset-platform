# Contrato de identidad, activos, IEC 81346 y RDF

## Identidades
`Asset.id=UUID` permanente, `tenant_id`, `project_id`, `class`, `status`, `valid_from`, `revision`. Separar `FunctionalObject`, `ProductObject`, `LocationObject`, tipos y designaciones IEC 81346 historizadas. `AssetReferenceDesignation` es dato mutable, no PK. ExternalRefs se escopan por `(tenant, provider, external_id)` y no producen duplicación.

## Relación semántica
`subject_uuid` -> `predicate_uri` -> `object_uuid` o typed literal. Predicados estándar solo si existen en ontología concreta (por ejemplo Brick `hasPoint`,`hasLocation`, `feeds`). Extensiones OAP usan namespace documentado; no inventar prefijos atribuidos a Brick. Property graph SQL+RDF projection; SPARQL solo sobre proyección autorizada.

## Versionado
Cada cambio de relación genera outbox con seq; worker RDF reconstruye named graph por tenant/proyecto, mantiene watermark y lag. Export Turtle/JSON-LD y validación SHACL; los consumidores pueden recibir projection_version y saber si están desactualizados.

## Migración y consultas
Crear `AssetTypeDefinition` JSON Schema y UI dynamic forms. Permitir funciones múltiples sin forzar parent único. Cuidar diferencias entre contención, ubicación, alimentación eléctrica y control. Evitar inferencias que generen acciones físicas sin aprobación.

## Tests
- Cambiar designación no altera UUID/historia/WO/telemetría.
- Un equipo tiene ubicación en dos escenas sin duplicación.
- Relaciones cruzadas entre tenants se rechazan.
- SHACL detecta point sin unidad o asset sin clasificación requerida; output legible.
