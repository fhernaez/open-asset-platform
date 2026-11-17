# Grafo de dependencias planificado (NO grafo extraído del código fuente)

```mermaid
flowchart TD
  UI[React frontend] --> API[Django REST+ASGI]
  API --> CORE[Identity Projects Assets Events]
  CORE --> DB[(PostgreSQL PostGIS)]
  API --> SP[Spatial/Semantics]
  SP --> CORE
  SP --> RDF[RDF projection worker]
  CORE --> PL[Plugin Manager]
  PL --> CMMS[CMMS addon]
  PL --> BMS[BMS addon]
  PL --> EMS[EMS addon]
  PL --> MQTT[MQTT addon]
  PL --> OTHER[Modbus BACnet HTTP Edge]
  MQTT --> TS[Telemetry worker]
  TS --> DB
  TS --> RULES[Rules/Alarm service]
  RULES --> CMD[Command Service]
  PL --> NR[Node-RED integration optional]
  PL --> ERP[ERP integration optional]
  PL --> AI[Local Assistant optional]
  PL --> MCP[MCP server optional]
```

Este esquema es arquitectura objetivo. **No debe confundirse con la extracción exigida de código OpenRemote/Atlas** (`docs/research/CODE_GRAPH_RUNBOOK.md`). El grafo real debe obtenerse tras descargar fuentes y fijar hashes con evidencia.

## Regla de dependencia
Addons dependen de interfaces `core.*` públicas; CORE jamás importa módulos de addons. `cmms` puede consumir `assets` por servicios autorizados, no consultar tablas privadas. `nodered` es optional y nunca ancestro obligatorio de MQTT ingestion. No permitir ciclos en manifest graph.
