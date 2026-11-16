# Recorridos Playwright E2E de aplicación

## E2E-A: Primer login y proyecto
Stack Compose healthy, bootstrap admin seguro -> login -> crear proyecto Tenant A -> asset tipo `Pump` -> atributo `temperature` -> modificar -> refresh -> sigue idéntico. Usuario Tenant B no lista asset.

## E2E-B: Plugin lifecycle
`.env` CMMS default false -> primer arranque UI disabled -> admin habilita -> visible CMMS menú/API -> shutdown/up -> sigue enabled -> lock de deploy `cmms` -> UI readonly y API 403, conservar override tras quitar lock.

## E2E-C: MQTT sampling
Crear MQTT Agent y topic; seleccionar on_change y maxN=2/PT1H; atributo storageDatapoint=true con override N=5; publish deterministic fixture; verify dashboard current, history sample counts, policy effective y reduce metrics, sin Node-RED.

## E2E-D: Mantenimiento
Desde asset crear WorkRequest -> approve -> WorkOrder -> assigned/in progress -> checklist+time+part -> complete -> close; historial asset y dashboard report correctos. Tenant B sin acceso.

## E2E-E: Escenas
Crear site rural geopoint, navega a edificio, sube planta PNG y esquema JPG, coloca asset en ambas; guarda/reload, mapas representaciones correctas; topología semántica sin cambios.

## E2E-F: Integraciones
Import JSON Node-RED preview -> commit -> export a tab nueva → Node-RED test instance lo acepta; desactivar plugin y MQTT continúa. ERP unavailable muestra request pending; MCP read scope no entrega secret, write proposal requiere aprobación.

## UX checklist
Responsive desktop/tablet/mobile; keyboard/accessibility labels, focus, contraste; timezone/localization ES/EN; errores empty/offline/loading; export status en cada operación; sin secrets en UI/devtools.
