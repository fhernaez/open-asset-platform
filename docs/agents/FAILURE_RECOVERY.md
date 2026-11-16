# Si Kilo pierde contexto, falla un test o se agota presupuesto

1. Abrir `docs/evidence/IMPLEMENTATION_STATUS.md` y `TASK_LOG.md`, inspeccionar archivos y `git status`; no asumir que cualquier respuesta anterior del chat se guardó.
2. Verificar `.venv` y ruta Python; evitar recrear dependencias si lock está bien.
3. Reproducir exactamente última prueba fallida con mismo fixture, recopilar error real y aislar cambio mínimo. Nunca saltar test ni remplazar integración por mock.
4. Revertir solo cambios propios causantes del problema, no borrar datos, volúmenes o código de terceros.
5. Si Docker/network/fuente no disponible, registrar BLOCKED con comando y salida y una alternativa offline verificable; no afirmar resultado futuro.
6. Dejar checkpoint claro para siguiente agente: estado y gate, pendientes por orden, cambios, riesgos, próximos comandos y pruebas.
