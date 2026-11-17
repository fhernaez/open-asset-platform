# Diagramas de flujo C4 lógico + escenarios operativos

## Flujo telemetría MQTT
```mermaid
flowchart LR
  D[Device] --> M[MQTT Broker]
  M --> I[Protocol Agent Ingest]
  I --> V[Validate and Normalize]
  V --> C[Latest State and Rules]
  C --> P{Storage Policy}
  P -->|Accepted| T[(PostgreSQL)]
  P -->|Filtered| X[Drop Metrics and Counters]
  C --> A[Alerts and Live Subscriptions]
  T --> Q[History API]
```
La política de almacenamiento NO es filtro de eventos de reglas ni actualizaciones de estado actual. Los eventos de comandos no se silencian por cuota de históricos.

## Flujo cambio de plugin
```mermaid
flowchart TD
  G[Admin GUI] --> E[REST Plugin Activation]
  E --> Z[AuthZ and Deploy Lock]
  Z --> D[(Plugin Activation DB)]
  D --> O[Outbox change event]
  O --> R[Workers Reconcile Runtime]
  R --> H[Health/Status API]
```
No tocar `INSTALLED_APPS` ni reiniciar desde GUI; si no instalado, comunicar `INSTALL_REQUIRED`.

## Flujo DB primera ejecución
```mermaid
flowchart TD
  C[Compose up] --> P[Postgres start]
  P --> B[DB bootstrap job idempotent]
  B --> M[Django migrate --noinput]
  M --> S[Seed defaults once]
  S --> API[Django API/web/workers]
```
`db-bootstrap` valida extensiones disponibles, roles/DB, scripts y permisos, aborta explícitamente si falta PostGIS.

## Flujo import/export Node-RED
1. Export JSON o Admin API (solo entorno test/autorizado) → parser estructural → propuesta de assets/points/relations → dedupe `external_ref` → preview diff/confirm → registro canónico.
2. Asset/puntos OAP → generador de flow JSON versionado → validar topología/nombres/no secrets → preview → `POST /flow` o `PUT /flow/:id` autorizado con hash de concurrencia. Node-RED mantiene ejecución, OAP semántica/identidad.

## Flujo MCP escritura
Prompt externo → MCP auth scopes → herramienta `propose_*` → diff firmado o expirable → validación de dominio/SHACL/roles → aprobación humana → comando idempotente → auditoría y respuesta; nunca write directa DB, nunca command físico implícito.
