# Recorrido funcional que define primera app utilizable

1. Operador `admin` inicia stack Docker en host limpio sin abrir terminal SQL, visita frontend y hace bootstrap seguro.
2. Crea organización, proyecto `Industrial Demo`, ubicación `Planta`, activo tipo `Pump`, punto `pressure` con unidad `kPa`.
3. Abre plugin manager, ve MQTT installed true/default enabled; crea `MQTT Agent`, subscription topic y parser JSON.
4. Define agent `storageDatapoint default on_change` y `max_samples=3/PT1H`; atributo `pressure` override a 5/PT1H. Editor muestra policy efectiva y origen.
5. MQTT test client publica 100 valores `1.0`, luego `2.0` (misma ventana); UI muestra current=2, history 2 filas, messages received=101 y skipped=99 (si tolerancia=0 y sin duplicates). Alarm engine recibe todas observaciones configuradas.
6. Desde frontend crea WorkRequest para bomba, aprueba WO y adjunta comentario/tarea. Muestra historial orden y asset con cross-links.
7. Admin desactiva CMMS desde UI, vista de activos y telemetría siguen operando; reactiva, datos WO conservados. Reboot Compose no revierte toggles.
8. Carga plano JPG y sitúa bomba, carga segunda imagen sin duplicar asset; en mapa GIS abre proyecto rural con coordenadas.
9. Exporta assets MQTT a Node-RED opcional y vuelve a importar JSON, sólo genera propuestas, sin secretos. ERP y MCP opcionales sin arruinar core.

**Primer milestone aceptable:** pasos 1-7 más smoke de paso 8 mínimo; S09 cubrirá resto de parity. Tests vinculantes E2E y métricas de base reales; reproducible sin equipamiento físico.
