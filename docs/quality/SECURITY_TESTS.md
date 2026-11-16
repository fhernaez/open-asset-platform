# Pruebas de seguridad negativas — por ruta/protocolo

## Authorization multitenancy
`SEC-001`: tenant A token + ID de asset B en GET/PATCH -> deny no leak. `SEC-002`: WS subscription de B -> deny. `SEC-003`: export RDF/SPARQL de B -> deny. `SEC-004`: GIS features de B -> deny. `SEC-005`: MCP tools sin scope de B -> deny. `SEC-006`: MQTT same-topic de broker no autorizado -> deny en ACL/device credential.

## Web/app
CSRF en endpoints cookie; XSS en labels, widgets, SVG; SQL injection/ORM raw query; SSRF en HTTP agent/webhook maps/Node-RED ERP; file upload path traversal/mime spoof/image bombs; rate limit login/OIDC callback; mass assignment plugin settings/roles; CORS y CSP; secret hidden in swagger/logs.

## Commands/AI
Command fuera rango, offline, read-only user, plugin disabled, time-expired y duplicate: no ejecución. Prompt injection en herramienta recuperada no puede solicitar secrets ni exfiltrar assets. MCP proposal aprobado solo por actor diferente/autorizado según policy, audit actor origin.

## DevSecOps
Scan de contenedores y deps, no passwords en `.env` sample ni Git; no docker socket en API; runtime unprivileged, TLS y ACL; dependabot/update policy auditado. Test Threat model antes de conectar hardware físico.

## Criterio de aprobación
Todas las pruebas críticas deben demostrar failure response seguro y ausencia de side effect, con logs sanitizados, test fixtures en CI y revisión manual. Un warning crítico no se rebaja sin explicación y aceptación formal de riesgo.
