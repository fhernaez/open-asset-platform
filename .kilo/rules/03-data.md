# Persistencia, series y seguridad
- PostgreSQL + PostGIS reales en integración. DB creada automáticamente primera vez y también si falta sobre volumen existente.
- Conectividad: Gateway como tipo de activo + GatewayBinding genérica (gateway→atributo, dirección + mapeo). Defaults por gateway -> overrides por atributo. ON CHANGE y N/período son MUST, no TODO. Atributos current state siempre se actualizan, aun cuando no se almacene la muestra.
- Config GUI persiste en DB; `.env` seed-once. Tenant isolation en toda consulta y comando. No logs de secrets ni datos personales innecesarios.
