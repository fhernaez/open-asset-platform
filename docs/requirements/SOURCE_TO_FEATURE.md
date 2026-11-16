# Funcionalidad a partir de fuentes (NO equivale a auditoría completa)

OpenRemote Core aporta referencia de: asset types/attributes, protocol agents MQTT/HTTP/WS/TCP/UDP/Modbus/BACnet cuando corresponda, dashboards, automation when-then/flow/JS/Groovy, multi-tenancy, users/roles, edge, REST/MQTT/WS APIs, automation y deployment. Validar versión/capacidad específica en repositorio, docs y tests por commit.

Atlas CMMS aporta referencia de: work orders/requests, maintenance plans, scheduling, teams, assignments, assets/locations, meters, parts/stock, vendors, costs/time, downtime, checklist, reports, notifications, triggers/webhooks, permissions. El README menciona funcionalidades comerciales dual licensed: inventariar sin asumir derecho de copiar código no publicado.

Nuestro producto agrega: IEC/ISO 81346 + Brick + Haystack RDF/SHACL, mapas por imágenes/GIS, MQTT almacenamiento solo cambios y N/period, bidireccional Node-RED, MCP, local AI, integración ERP en lugar de backend de compras y configuración de plugins por GUI.

## Cómo auditar sin inventar
- Fijar hash de ambos repositorios; enumerar módulos/configuración de build; clases/servicios; endpoints/OpenAPI; modelos de datos; eventos; tests.
- Clasificar: VERIFIED_SOURCE, VERIFIED_DOCS_ONLY, COMMERCIAL_UNAVAILABLE, NEW_REQUIREMENT, UNKNOWN.
- Generar matriz de 1 feature → source path + symbol + API + fixture + acceptance. Tests del código original no validan automáticamente nuestro reemplazo.
