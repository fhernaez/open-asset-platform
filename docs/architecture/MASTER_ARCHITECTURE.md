# Arquitectura maestra — OAP autonomous FOSS

## 1. Propósito, alcance y criterio de arquitectura
Construir un producto autosuficiente que reimplemente y amplíe capacidades IoT/BMS de OpenRemote y CMMS de Atlas. El backend Django es propietario del modelo maestro; no existe componente OpenRemote/Atlas ejecutándose en producción. No se alcanza «paridad» por tener menús con mismos nombres: cada capacidad exige contrato funcional, integración y prueba end-to-end documentada. Definir reemplazos originales para funcionalidades no disponibles bajo licencias abiertas.

## 2. Contexto C4 — actores y sistemas
Actores: operador de edificio, mantenimiento, técnico de campo, administrador tenant, administrador de plataforma, integrador IoT, servicio ERP, agente MCP, auditor. Sistemas externos: dispositivo/broker MQTT, BACnet/IP, Modbus TCP/RTU, HTTP, KNX/otros por adaptador; Node-RED opcional; ERP autoridad comercial; OIDC/Keycloak opcional; proveedor de mapas; LLM local. OAP proporciona REST, WebSocket/SSE, MCP (desplegable), exportación semántica/gis, UI y alertas.

## 3. Contenedores lógicos
```
Browser React MapLibre dashboards admin plugins
     | HTTPS/OIDC/session
Django DRF + ASGI CORE -----> websocket/SSE subscription
     | ORM transactions/outbox
     +----> PostgreSQL PostGIS
     +----> semantic projection worker --> RDF (rebuildable)
     +----> notification/CMMS/rules workers
     +----> plugins in-process: CMMS BMS EMS Analytics
     +----> protocol & integration services (MQTT/Modbus/BACnet/HTTP/Edge)
     +----> optional local assistant, MCP, ERP, Node-RED connectors
```
Los procesos IoT no dependen de las solicitudes HTTP. Las colas no garantizan exactamente una entrega: outbox transaccional, retries idempotentes, claves externas de deduplicación y DLQ cuando aplique.

## 4. Bounded contexts
- **Platform**: organización, proyecto, identidad, permisos, configuración, auditoría, extensión.
- **Asset Registry**: activos/productos/funciones/ubicaciones, identificadores históricos, tipologías (incl. tipo `gateway`), puntos y relaciones.
- **Connectivity**: gateways por protocolo (MQTT/Modbus/OPC-UA/BACnet/SNMP/CAN) como activos especiales, bindings genéricas gateway→atributo (dirección + mapeo), adapters del worker de ingesta (ADR-014).
- **Semantics**: IEC 81346 referencia/aspectos, tipos Brick/Haystack, ontologías extensibles, RDF, SHACL.
- **Spatial**: escenas/CRS/capas/transformaciones/placements; complementa, no sustituye ubicación semántica.
- **Telemetry**: ingesta, calidad, estado actual y series retenidas; historial por política configurable agente/atributo.
- **Rules & Commands**: condiciones, automatización, alarmas, permisos de actuación, interlocks, auditoría.
- **CMMS**: órdenes, planes, solicitudes, partes, recursos; ERP fuente de compras.
- **BMS/EMS**: operaciones edificios/energía, horarios, visualización y métricas.
- **Integrations**: conectores externos con contratos, secretos, mapeos y salud.

## 5. Regla única de autoridad
`Asset.id` UUID inmutable es identificador canónico. El equipo físico, la función y la ubicación son objetos/relaciones diferenciados. No usar la referencia IEC como PK. PostgreSQL guarda master, estados transaccionales y muestras aceptadas (histórico); RDF es proyección eventual reconstruible con watermark y reintentos. Node-RED guarda flujos, no inventario maestro. ERP compra/factura, OAP solicitud de recurso y referencia externa.

## 6. Composición y operación
La imagen Django incluye apps CORE y addons Django autorizados; `INSTALLED_APPS` se fija al build/arranque. El plugin manager persiste `PluginDefinition`, `PluginActivation`, `PluginSettings`, health y audit y puede habilitar por tenant/proyecto sin editar Python importado. Instalar nuevo código o cambiar modelos requiere release+migración+restart. Drivers no confiables, asistentes, MCP, gateways se aíslan como servicios Docker. Frontend shell registra extensiones mediante `UIExtensionManifest` versionado (menús, rutas, widgets, formularios, capas).

## 7. Datos y DB
PostgreSQL con extensión `postgis` (imagen auditada); tipos `jsonb`, relaciones y constraints; índice compuesto `(tenant_id, project_id, id)` según tablas. UUID para muestras. Tabla de historial con índice `(attribute_id, ts DESC)`, tiempo en UTC y dedupe por source/event ID; tabla current value separada. Retención por borrado de ventanas vencidas (ver `docs/infrastructure/DB_BOOTSTRAP.md` y `docs/core/TELEMETRY_POLICY.md`).

## 8. Protocolos
MQTT directo e integrado (sin Node-RED) con agent profiles. Workers de ingesta actualizan current value, evalúan reglas/alarma y A CONTINUACIÓN aplican StoragePolicy. Modbus TCP/RTU, BACnet/IP, HTTP/WS, SNMP y Edge según etapas; drivers de seguridad física separados. Provisionamiento/Discovery, punto ↔ equipo semántico, ACL por dispositivo, quality flags, QoS y retry. No prometer soportar absolutamente todo protocolo sin especificar gateway.

## 9. API, UI y MCP
DRF OpenAPI v1, versiones de eventos, problem details unificado, paginación y filtros por proyecto. WebSockets/SSE se autentican y filtran antes de publicar. React/TypeScript con dashboards editor, mapa escena/mapa, gestor activos, alarmas, administración plugin y assistant UI. MCP es vista de herramientas de dominio con scopes, consentimiento y aprobación; no acceso directo DB ni comandos físicos arbitrarios. UI/REST/MCP comparten la misma autorización de negocio.

### 9.1 Navegación (menú canónico — ADR-014)

El menú se define aquí y se deriva a `frontend/src/features/flags.ts`; las specs y prompts lo referencian (fuente única):

1. **Activos** — árbol, tipologías (incl. `gateway`), plantillas, atributos, designaciones.
2. **Conectividad** — gateways por protocolo, bindings, discovery, estado de workers.
3. **Telemetría** — current, historial, stats de ingesta, políticas de almacenamiento.
4. **Dashboards** — builder, widgets (línea/gauge/card/tabla), widget de mapa (plano+geo).
5. **Mapas** — escenas por imágenes, capas, MapLibre geo, placement de activos.
6. **Reglas** — reglas/alarmas/schedules/editor de flujos.
7. **CMMS** — mantenimiento.
8. **Integraciones** — Node-RED, ERP.
9. **IA/MCP** — asistente local, MCP.
10. **Administración** — plugins, usuarios/roles/realms, settings, auditoría, logs.

Regla: una sección sin implementación real se muestra "disponible en etapa X" (feature flags por gate); nunca controles rotos.

## 10. Seguridad operacional
Autenticación OIDC o local inicial segura; RBAC+ABAC tenant/project, roles y token scopes; política fail-closed. Comandos a actuadores: validación límites/rangos, interlocks, TTL, idempotencia, doble confirmación donde corresponda, permisos, visibilidad de fallos y auditoría. Pruebas HIL antes de puesta en producción. Errores/telemetría no deben inundar almacenamiento por efectos en cascada.

## 11. Escalabilidad
Primer despliegue: monolito modular + workers separados, no microservicios por entidad. Escalado por procesos si el throughput lo justifica: MQTT ingestion workers por partición/tenant, writer batched, jobs idempotentes, cachés y queries paginadas. Retention/compaction y policy de tasa por atributo reducen presión de TSDB. Monitorizar lag, drops, DLQ, disk, cardinalidad, consultas lentas.

## 12. Deploy y actualización
Docker Compose base + perfiles; esquema datos primero: DB init idempotente con volumen nuevo Y existente, migrations/versionado, seed de plugins once, api/web, workers. Healthcheck para DB; migrator one-shot `service_completed_successfully`; no migrations al iniciar cada worker. Backup antes de upgrade, expand/contract en migraciones, rollback de código con compatibilidad, restauración probada. Las configuraciones administrativas persisten por encima de defaults env; locks de seguridad env siempre prevalecen.

## 13. FOSS + documentación pública
Revisar licencias de cada paquete, assets UI, modelos IA y extensiones Postgres. Licencia OAP definida en ADR tras auditoría; cualquier reutilización AGPL conserva obligaciones. No copiar descripciones enteras ni código de características solo comerciales. GitHub almacena `docs/`, infraestructura, código, tests, CI, migrations y SBOM. Secretos/volúmenes no versionados.

## 14. Criterios globales de aceptación
G0 especificaciones, G1 sandbox+DB+stack, G2 modelo/tenant, G3 plugin toggles/restart, G4 MQTT on_change/N período, G5 CMMS, G6 GIS/semántica, G7 protocolos+reglas, G8 integraciones+MCP, G9 seguridad/performance/restore/paridad. Definidos y bloqueantes en `docs/quality/GATES.md`. Sin tests ejecutados, status BLOCKED.
