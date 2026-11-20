# Análisis de acercamiento a las normativas (81346 / Haystack / Brick / RDF-SHACL)

Fecha: 2026-11-19. Estado honesto del grado de acercamiento y plan de cierre de brechas.

## 1. IEC/ISO 81346 (RDS por aspectos =/-/+/%)

| Elemento | Estado actual | Plan |
|---|---|---|
| Designación por aspectos (función/producto/ubicación/tipo) | ❌ sin implementar | `Asset.designations` versionado con `{aspect: {code, occurrence}}`; códigos 1-3 letras + número de ocurrencia auto-sugerido (único por tenant/ámbito) |
| Árbol de navegación por taxonomía | ⚠️ jerarquía `parent` existe, sin RDS | Árbol agrupable/ordenable por aspecto; drag&drop con validación |
| Conformidad 81346-12 plena | ❌ | Límite documentado: la norma requiere compra; usamos la convención SIN certificar conformidad |

## 2. Project Haystack (tags) y Xeto

| Elemento | Estado actual | Plan |
|---|---|---|
| Etiquetado de equipos/puntos | ✅ parcial: `metadata.brick` en catálogo | Extender a tags Haystack (`haystack: [ahu, discharge, air, temp, sensor]`) en manifiestos y atributos descubiertos |
| API estándar de consulta | ❌ | Fuera de alcance por ahora (contratos propios OpenAPI); documentado |
| Validación tipo Xeto | ❌ | Cubierto por `rules` declarativas en manifiestos (equivalente funcional, no Xeto nativo) |

## 3. Brick Schema (ontología)

| Elemento | Estado actual | Plan |
|---|---|---|
| Clases tipadas de equipos/puntos | ✅ parcial: tags Brick en catálogo | Clases completas en manifiestos; `is_location` para espacios |
| Relaciones (feeds/hasPoint/isPartOf/isFedBy) | ❌ | Relaciones declaradas en `rules` y proyectadas a RDF (brick:feeds, brick:hasPoint, brick:isPartOf) |

## 4. RDF y SHACL

| Elemento | Estado actual | Plan |
|---|---|---|
| Tripletas RDF | ❌ | `export_rdf` (rdflib) con namespaces brick/haystack/81346: asset→punto→relaciones |
| Validación SHACL | ❌ | `validate_semantics` (pyshacl) sobre el grafo proyectado; reglas declarativas en manifiestos evaluadas en línea de escritura |
| Consultas SPARQL | ❌ | Fuera de alcance en línea de escritura (proyección offline); documentado |

## Conclusión

Las brechas principales son: designaciones 81346, relaciones Brick, proyección/validación RDF-SHACL, y el etiquetado Haystack completo. Se cierran en esta iteración con el modelo declarativo (manifiestos + rules + proyección), sin certificación de conformidad y sin triplestore en línea de escritura (documentado como límite).
