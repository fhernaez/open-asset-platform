# Matriz de paridad — OpenRemote Core (objetivo, pendiente de auditoría completa)

| Área | Capacidades a contrastar contra fuente fijada | Destino OAP | Pruebas esperadas | Estado |
|---|---|---|---|---|
| Asset manager | jerarquías, tipos dinámicos, metadata, atributos, agent links, búsqueda, templates | CORE Asset | CRUD+schema+auth+bulk | TO_AUDIT |
| MQTT | agent/subscriptions/mapping/topics/qos/broker, estado y escritura | plugin MQTT | publish/subscribe+loss/reconnect | TO_AUDIT |
| Protocol agents | HTTP, WebSocket, TCP/UDP, SNMP, Modbus, BACnet, KNX, Zigbee/Z-Wave y otros realmente presentes | protocolo plugins | fixture por adaptador | TO_AUDIT |
| Rules | when-then, flow-based, JS/Groovy, alarms, conditions, schedules | Rules Engine | regla ejecutada, timers y alertas | TO_AUDIT |
| Dashboards | charts, widgets, editor, data, themes, permissions | Dashboards | UI CRUD+render+isolation | TO_AUDIT |
| Identity | realms, service accounts, auth, roles, users | CORE Identity | matrix RBAC tenant deny | TO_AUDIT |
| Edge | gateways, offline operations, sync and provisioning | Edge | partition/replay/conflict | TO_AUDIT |
| APIs | HTTP/REST, MQTT, WS | API/Gateways | contract+auth+rate | TO_AUDIT |
| Persistence | datapoint retention, event history, metadata | TimescaleDB | durability+recovery+policy | TO_AUDIT |
| Manager UI | asset tree, attribute configuration, maps, users, rule editor | React shell | E2E workflows | TO_AUDIT |
| Commercial/hosted differences | verificar solo con fuentes autorizadas | implementaciones originales | spec independiente | TO_AUDIT |

**Importante:** la lista de protocolos es inventario de candidatos, NO afirmación de que todos estén disponibles o soportados en un commit determinado. La auditoría deberá identificar diferencias reales y orden de implementación. `docs/research/CODE_GRAPH_RUNBOOK.md`.
