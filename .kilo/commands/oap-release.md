# Preparar una release verificable
1. Validar cierre G0-G9 aplicable; comprobar migraciones, backup/restore, security, licensing, SBOM, dev/prod Compose, AI/MCP disabled by default.
2. Ejecutar smoke en Compose limpio, reboot con volumen persistente, tests y documentar outputs.
3. Fijar versiones, CHANGELOG, imágenes por digest, decisiones pendientes y limitaciones conocidas.
4. No declarar paridad total hasta superar la matriz de referencia.
