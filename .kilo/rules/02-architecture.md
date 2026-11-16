# Límites de arquitectura
- Django/DRF/GeoDjango es el CORE. OpenRemote/Atlas no son runtime. Plugins referencian servicios publicados del núcleo, no sus modelos/DB privados.
- Un único Asset UUID. Semántica, grafos y geometría no duplican identidad. RDF es proyección con coherencia eventual medible.
- Transportes y workers desacoplados de request HTTP. Procesamiento de telemetría antes de persistencia; controles de seguridad antes de comandos físicos.
- Cada cambio de contrato requiere versión, ADR si rompe arquitectura y contract tests.
