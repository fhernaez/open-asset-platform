# Backlog estructurado de funcionalidades — revisar durante auditoría

## Plataforma y data
Multitenancy realms/organizations; asset types custom, attributes dynamic, designations, templates, bulk imports, API, GIS/histories, dashboards, plugin admin, notifications, audit, identity. Prioridades P0 para identidad/modelo/instalación/MQTT policy, P1 para BMS/CMMS GIS, P2 extensiones protocolos.

## Protocolos
MQTT/HTTP/WS, TCP/UDP, SNMP, Modbus TCP/RTU, BACnet/IP, KNX, Zigbee2MQTT, OPC UA, Edge/provisioning, discovery, mapping, validation, command interlocks, device certificate rotation. Contrastar cada adaptador con fuente OpenRemote por commit antes de declarar paridad.

## Automatización
When/then, reglas declarativas, schedules, alarm acknowledgements, alerts/dedupe, flow-based editor si se justifica, scripting sandboxed si existe demanda y se puede asegurar, notifications, notifications destinations, dashboards/insights; evaluar gap JS/Groovy de OpenRemote sin ejecutar lenguajes peligrosos directamente.

## Mantenimiento
Requests, approval, WO, preventive by calendar/meter/condition, teams/technicians/contractors, priority/SLA, downtime, parts, min stock, time log, cost, attachment, checklist, vendors, locations, reports, webhooks; ERP requisition en lugar de submódulo compras. Auditar características Atlas incluyendo mobile y comerciales por separado.

## Novedades OAP
RDF/SHACL, IEC/ISO 81346/Brick/Haystack, escenas local+geo+diagramas, MQTT on_change/maxN per window en Agent/Attribute, Node-RED bidirectional JSON, local assistant/MCP, standalone Docker DB autocreation + admin plugin GUI. Ninguna nueva capacidad requiere mantener OpenRemote.

## Definition of priority
P0 bloquea S01-04; P1 bloquea etapa correspondiente; P2 sigue siendo requisito para paridad total pero no bloquea MVP. Cada tarea debe tener un test ID, owner, estado y commit de referencia.
