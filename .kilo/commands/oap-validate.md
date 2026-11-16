# Ejecutar validaciones concretas
1. Ejecutar `.venv/bin/python scripts/check_spec_kit.py` para kit.
2. Ejecutar `bash scripts/quality_gate.sh` para código construido; SI falla, bloquear despliegue.
3. Ejecutar pruebas de Docker DB-bootstrap en volumen limpio Y existente sin BD, MQTT storage-policy, plugins restart, integración y UI según gate.
4. Guardar logs/comandos reales y actualizar estado. No decir PASS si gate no se ejecutó.
