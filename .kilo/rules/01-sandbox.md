# Sandbox obligatorio
- Antes de cualquier instalación/ejecución de Python local: `python3 -m venv .venv` (si no existe), verificar ruta y ejecutar SIEMPRE `.venv/bin/python`.
- No modificar sistema anfitrión, sudo, redes externas, servicios reales, credenciales ni dispositivo físico sin autorización.
- Docker images reproducibles y secrets aislados. No instalar dependencias ad hoc sin actualizar manifests/lockfiles.
- Los scripts son idempotentes y de mínimo privilegio. Prohibido destruir volúmenes para corregir errores de arranque.
