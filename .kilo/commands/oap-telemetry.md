# Prueba obligatoria política almacenamiento MQTT
1. Leer `docs/core/TELEMETRY_POLICY.md` y `docs/quality/TELEMETRY_CASES.md`.
2. Definir un MQTT Agent con policy default `on_change` y Attribute con override `max_n_per_window`.
3. Publicar series deterministas en broker real; comparar cantidad de mensajes recibidos, estado actual, mediciones persistidas, alertas y counters.
4. Correr escenarios NaN/null/out-of-order/restart/ventana/desconexión. No aceptar test con datos inventados.
