# ADR: Stack semántico (81346 + Brick/Haystack + RDF/SHACL)

Estado: **Aceptada** (2026-11-19).

## Contexto

Los 4 estándares son complementarios: 81346 nombra/jerarquiza, Haystack/Brick dan metadatos operativos, RDF/SHACL dan estructura y validación. El gap-analysis (`docs/research/STANDARDS_GAP_ANALYSIS.md`) marca las brechas.

## Decisión

1. **81346**: designaciones versionadas en `Asset.designations` por aspecto (`=function`, `-product`, `+location`, `%type`), códigos 1-3 letras + número de ocurrencia auto-sugerido (único por tenant/ámbito). Conformidad 81346-12 plena NO certificable (norma de pago): límite documentado.
2. **Metadatos**: los manifiestos declaran `brick` y `haystack` (tags); los atributos descubiertos heredan tags por tipo/valor.
3. **Reglas de validación** (SHACL-like, en línea de escritura): `rules` en manifiestos — atributos requeridos y relaciones requeridas (ej. VAV exige airflow_sensor e isFedBy→AHU); se evalúan al crear/importar y devuelven 422 con detalle.
4. **Proyección RDF** (offline): `export_rdf` con rdflib (namespaces brick/haystack/81346); `validate_semantics` con pyshacl sobre el grafo proyectado. Sin triplestore en línea de escritura (documentado como límite).

## Consecuencias

- Dependencias: `rdflib`, `pyshacl`.
- El catálogo semilla gana `is_location`, `rules`, `haystack` y clases Brick completas.

## Alternativas consideradas

- Triplestore + SPARQL en línea: rechazado (complejidad operativa; la proyección eventual cumple el objetivo).
- Xeto nativo: rechazado (equivalente funcional con reglas propias).
