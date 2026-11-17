# Funcionalidad a partir de fuentes (auditoría ejecutada 2026-11-17)

Inventario por paths en `docs/research/GRAPH_SOURCE_INDEX.md`; commits fijados en `docs/research/REFERENCE_LOCK.md`.

## OpenRemote Core (commit `6d46b473`) — clasificación

- **VERIFIED_SOURCE:** asset manager (árbol/tipos/links), atributos tipados con estado, datapoints con intervalos/periodos y export, reglas por scope (Global/Realm/Asset) + alarmas, editor de flujos JSON (Flow/Node/Wire), dashboards con widgets, mapas GeoJSON, gateway/edge con túneles, provisioning X509, notificaciones, realms/roles/usuarios, 19 protocol agents (MQTT/Modbus/HTTP/WS/SNMP/TCP/UDP/KNX/Z-Wave/Zigbee/LoRaWAN/Bluetooth/…), Manager UI con 17 páginas.
- **NEW_REQUIREMENT (OAP):** storage policies on_change + N/ventana T por agente/atributo, IEC/ISO 81346 + Brick/Haystack RDF/SHACL, Node-RED bidireccional, MCP + IA local, ERP integrado, GIS por imágenes locales + MapLibre.
- **Licencia:** CDDL-1.0 + GPL-2.0 (Classpath exception) + Timescale TSL (confirma que la dependencia TimescaleDB está bajo TSL — OAP la evita, ADR-013).

## Atlas CMMS (`Grashjs/cmms`, commit `06abfe35`) — clasificación

- **VERIFIED_SOURCE:** work orders/requests/portal, preventivo (calendario/medidor), inventario (partes/stock/multi), purchase orders, meters/readings, labor/time/cost, checklist, adjuntos (MinIO), downtime, teams/turnos/schedules, vendors/customers, locations + floor plans, analytics (WO/asset/part/request/user), custom fields/field configuration, workflows, import/export, notificaciones/webhooks, PWA móvil.
- **COMMERCIAL_UNAVAILABLE:** white-label/branding, SSO, LDAP, enterprise features (`LicenseService.hasEntitlement` + `LICENSE_KEY`). OAP NO copia estos módulos; implementa equivalentes originales solo si se priorizan.
- **Decisión OAP:** compras se implementan como requisiciones a ERP externo (OAP-ERP-001), no como submódulo interno.

## Nuestro producto agrega (NEW_REQUIREMENT)

IEC/ISO 81346 + Brick + Haystack RDF/SHACL; mapas por imágenes/GIS; MQTT con almacenamiento solo cambios y N/periodo; Node-RED bidireccional; MCP; IA local opt-in; integración ERP; configuración de plugins por GUI; DB autoprovisionada en primer deploy.

## Cómo auditar sin inventar (procedimiento)

1. Fijar hash en `REFERENCE_LOCK.md` (ya fijados ambos repos).
2. Enumerar módulos/configuración de build, clases/servicios, endpoints/OpenAPI, modelos, eventos, tests.
3. Clasificar: `VERIFIED_SOURCE`, `VERIFIED_DOCS_ONLY`, `COMMERCIAL_UNAVAILABLE`, `NEW_REQUIREMENT`, `UNKNOWN`.
4. Matriz 1 feature → source path + símbolo + API + fixture + acceptance. Los tests del código original NO validan nuestro reemplazo: cada fila exige test propio con evidencia.
