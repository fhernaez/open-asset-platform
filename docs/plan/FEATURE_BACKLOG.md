# Backlog estructurado de funcionalidades — v2 (auditado 2026-11-17)

Prioridades re-evaluadas con el inventario real de `openremote/core` @ `6d46b473` y `Grashjs/cmms` @ `06abfe35` (ver `GRAPH_SOURCE_INDEX.md`).

## Plataforma y data (OAP-PLT / OAP-ASS / OAP-OPS)

Multitenancy realms/orgs; asset types custom, attributes dinámicos tipados, designaciones, plantillas, bulk import, API OpenAPI, historiales, dashboards, plugin admin, notificaciones, auditoría, identidad (OIDC futuro).
**P0:** identidad/modelo/instalación/UI shell/MQTT policy · **P1:** notificaciones, realms, export, plantillas · **P2:** SSO/OIDC, white-label original.

## Telemetría y almacenamiento (OAP-TEL / OAP-MQT) — diferenciador OAP

Current value, historial con export, agregación por intervalo/periodo, storage policies `on_change` + `N/ventana T` por agente y atributo, dedupe/replay, métricas de ingesta, retención.
**P0:** todo lo de G4 (TEL-001..020) · **P1:** agregación periódica, export · **P2:** retención automatizada.

## Protocolos (OAP-PRO)

MQTT/HTTP/WS, Modbus TCP/RTU, BACnet/IP, Edge/provisioning, simuladores. Larga cola P2: KNX, Z-Wave, Zigbee, SNMP, TCP/UDP, LoRaWAN, Bluetooth, Velbus, ArtNet, tradfri (verificados en OpenRemote).
**P0:** MQTT (G4) · **P1:** Modbus/BACnet/HTTP/Edge (G7) · **P2:** larga cola (G9).

## Automatización (OAP-RUL)

When/then, reglas por scope, alarmas con acknowledge, schedules, editor de flujos declarativo, notificaciones; evaluar scripting sandboxed solo si hay demanda verificable.
**P0:** — · **P1:** reglas/alarmas/schedules (G7) · **P2:** editor de flujos, scripting.

## Mantenimiento (OAP-CMM) — paridad Atlas verificada

Requests (+portal), WO (estados/asignaciones/tiempos), preventivo calendario/medidor/condición, teams/turnos, inventario (stock/movimientos), labor/costos, checklist/adjuntos, downtime, meters/readings, vendors/customers, locations + floor plans, analytics, custom fields, workflows, import/export, webhooks, PWA móvil.
**P0:** WO/requests/preventivo/inventario (G5) · **P1:** analytics, custom fields, meters, labor · **P2:** workflows, import/export, móvil.

## BMS/EMS (OAP-BMS / OAP-EMS)

HVAC, iluminación, schedules, escenas; energía, KPIs, tarifas, reportes.
**P1:** BMS/EMS básico (G7) · **P2:** optimización/peak-shaving (G9).

## Semántica y GIS (OAP-SEM / OAP-GIS)

IEC/ISO 81346 (historial), Brick/Haystack RDF/SHACL; escenas por imágenes + MapLibre/PostGIS + overlays.
**P1:** todo (G6).

## Dashboards (OAP-DSH)

Editor con widgets (chart/gauge/barchart/card), grid, permisos, GIS embebido, insights con muestras decimadas honestas.
**P1:** todo (G6).

## Integraciones e IA (OAP-NRD / OAP-ERP / OAP-AIM)

Node-RED import/export bidireccional + triggers; ERP requisiciones idempotentes; MCP con aprobación; asistente local opt-in.
**P1:** Node-RED/ERP/MCP (G8) · **P2:** asistente LLM.

## Frontend (OAP-UI) — rebuild total

Shell único (Ant Design + ECharts + Router + TanStack Query), mocks MSW por contrato, feature flags por gate, E2E Playwright. Pantallas: identity, asset manager, telemetría, MQTT, dashboards, GIS, reglas, CMMS, Node-RED, AI, admin.
**P0:** shell + asset manager + telemetría + MQTT + admin plugins (G2-G4) · **P1:** CMMS, dashboards, GIS, reglas (G5-G7) · **P2:** Node-RED, AI, export, settings avanzadas (G8-G9).

## Definition of priority

P0 bloquea G2-G4; P1 bloquea su gate (G5-G7); P2 es requisito de paridad total pero no bloquea MVP. Cada tarea debe tener test ID, owner, estado y commit de referencia en `TRACEABILITY.md`.
