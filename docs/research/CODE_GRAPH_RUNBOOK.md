# Extracción de grafo de código de repositorios de referencia

## Objetivos
El usuario requiere grafo real de dependencias, clases y funcionalidades. Un diagrama de arquitectura inventado no cumple. Se requiere fijar commit, ejecutar herramientas de análisis autorizadas dentro de sandbox y guardar artefactos reproducibles (paths + comandos) en `research/` excluyendo código de terceros no autorizable.

## Fuente OpenRemote Java/Gradle
- Checkout fijado con hash y confirmar submódulos. Obtener árbol de Gradle, imports Java/Kotlin, dependencias Gradle, módulos npm, modelos JPA, routes REST/WebSocket, eventos y agentes.
- Exportar `nodes.csv` (module,class,api,event,entity) y `edges.csv` (imports,calls,owns,emits,subscribes,queries), fuentes paths+líneas cuando posible.
- Usar herramientas documentadas (jdeps, Gradle dependencies, parser de AST, etc.) y reportar limitaciones de reflexión/inyección.

## Fuente Atlas Java/Spring + React
- Checkout fijado, `mvn dependency:tree` cuando sea seguro, package.json y TS imports, endpoints controller/services/repos/entities, migraciones Liquibase, roles y permisos.
- Grafo frontend ↔ API endpoint ↔ service ↔ model y flujos work order/inventory.

## Resultados
1. `docs/research/GRAPH_SOURCE_INDEX.md` con hashes y conteos verificables.
2. `research/graphs/source_nodes.csv`, `source_edges.csv`, `module-deps.mmd`, `feature-links.csv` y reporte de nodos no resueltos.
3. `PARITY_OPENREMOTE.md`, `PARITY_ATLAS.md` enlazando features verificadas.
4. Anotar NO DISPONIBLE/comercial cuando falte código; no burlar controles de licencias.

## Quality Gate
Debe existir evidencia ejecutada del parser y una muestra de verificación manual de edges; si no es posible descargar/clonar, declarar bloqueado y continuar con requisitos nuevos diseñados, nunca declarar que se extrajo el grafo.
