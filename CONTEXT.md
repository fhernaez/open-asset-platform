# Contexto persistente para Kilo Code: Open Asset Platform

## Objetivo innegociable
Construir desde cero una plataforma modular, autohospedable, FOSS y dockerizada, funcionalmente competitiva con la referencia **OpenRemote Core** y **Atlas CMMS**, sin ejecutar sus servidores en producción. El usuario prioriza capacidad, mantenimiento y escalabilidad sobre un prototipo meramente ilustrativo. El producto debe ser configurable por proyecto en sectores hotelero, industrial, eléctrico, urbano y rural.

## Decisiones cerradas
1. Framework Python: **Django + Django REST Framework**, no FastAPI como framework principal. Integración ASGI si se justifica. Python local **SIEMPRE** en `.venv` creado primero.
2. Base de datos: **PostgreSQL con TimescaleDB y PostGIS**; autocreación e inicialización en primer despliegue Docker. La BD única es autoridad operacional; RDF es proyección semántica reconstruible.
3. Modelo: IEC/ISO 81346 + Brick + Haystack, ontología de extensiones propia (`oap:`), validación SHACL, representaciones RDF y semántica/versionado.
4. GIS: escenas y capas a partir de una o múltiples imágenes (locales o georreferenciadas) y coordenadas geográficas (MapLibre y mapas opcionales). Referencia estable a activos.
5. Plugins: CORE pequeño y estable, addons BMS, EMS, CMMS, conectores MQTT/BACnet/Modbus/HTTP/Node-RED/ERP, asistente local, MCP. Habilitación desde `.env` al bootstrap y posteriormente GUI persistida; nunca sobrescribir en restart.
6. Telemetría crítica: `storageDatapoint` con ON CHANGE y tasa N POR PERÍODO, definibles tanto en MQTT Agent como en cada atributo. MQTT debe funcionar directamente sin Node-RED. Métricas de descarte/filtrado para observabilidad.
7. Node-RED opcional: importación de activos desde JSON/flows y exportación a una pestaña versionada; ejecuciones por webhook/MQTT, sin ser pipeline obligatorio.
8. ERP externo autoridad de compras, OAP CMMS de requerimientos técnicos y referencias a ERP; no construir contabilidad/OC nativa como requisito básico.
9. Agente local opcional (Ollama o alternativa), MCP de lectura y herramientas de escritura con aprobación y RBAC.
10. Docker Compose primero, imágenes publicables en GitHub, código y documentación versionados, CI con pruebas y checks de seguridad; no prometer upgrades sin pruebas.

## Interpretaciones de alcance
- “Todas las funcionalidades” se trata como **meta de paridad** y backlog exhaustivo con pruebas, no como una única entrega monolítica. Se deben verificar capacidades efectivamente presentes en repositorios de referencia y distinguir features comerciales no publicadas.
- Ninguna dependencia AGPL/TSL/comercial se introduce sin revisión de licencia. La implementación propietaria no se libera “quitando restricciones”.
- El sistema maestro no puede duplicar ID de activos con Node-RED, CMMS o gateways. Cada actor tiene autoridad clara sobre sus datos.

## Leer antes de codificar
`docs/core/TELEMETRY_POLICY.md` > `docs/infrastructure/DB_BOOTSTRAP.md` > `docs/contracts/PLUGIN_CONTRACT.md` > `docs/quality/GATES.md` > módulo específico y sus tests. No substituir documentación por supuestos.
