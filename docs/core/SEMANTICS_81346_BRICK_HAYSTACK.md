# CORE / Semantics 81346 Brick Haystack

## Objetivo de producto y límites de propiedad
Contrato de modelado común a edificio, IoT rural, redes urbanas, energía e industria; RDF como proyección semántica y SHACL para validar.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `TechnicalObject(id UUID, object_aspect=function/product/location/type)`.
- `ReferenceDesignation(object_id, standard_part, aspect, code, scope, valid_from)`.
- `SemanticType(uri, ontology, version)`.
- `SemanticAssertion(subject_uri, predicate_uri, object_uri/literal)`.
- `RdfProjectionCheckpoint(tenant, change_seq, lag, errors)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `POST /api/v1/semantics/designations:validate`.
- `GET /api/v1/assets/{id}/semantic`.
- `GET /api/v1/semantic/export?format=turtle`.
- `POST /api/v1/semantics/shacl:validate`.
- `POST /api/v1/semantics/projections:rebuild (admin only)`.

## Invariantes funcionales / reglas de negocio
- Designación IEC no se usa como identificador único global; funcional/producto/localización pueden coexistir.
- Utilizar clases Brick y definiciones Haystack cuando proceda; `oap:` para predicados propios, sin falsear prefijos.
- RDF se reconstruye desde PostgreSQL mediante outbox, con watermark/lag.
- No importar normas IEC/ISO protegidas a GitHub.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Cambiar ubicación conserva UUID y designación histórica.
- [ ] Una bomba con sensor y tablero produce triples y pasa SHACL.
- [ ] Missing required semantic property genera violation legible.
- [ ] Rebuild RDF idempotente y tenant A no consulta B.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
