# Operación: backup, restauración y upgrades

## Backup y protección
Backup PostgreSQL consistente incluyendo schemas, extensiones, roles/schema y app configuration; copiar archivos/uploads y exportar version de plugins, schemas y modelo semántico. Encriptar respaldos y configurar retención. No incluir secretos en claro ni confiar solo en volume snapshots sin pruebas.

## Restauración ensayada
Restore en stack aislado con misma versión de DB+extensiones, migrar si procede, validar total assets/orders/telemetry, sample policies, geo placements, plugin toggles, RDF projection watermark, permisos y health. No ejecutar restore sobre producción sin revisión de impacto.

## Upgrade
- Antes: pin version/digest, backup, comparar schema API/DB y dependencias addons.
- Migraciones expand: agregar columnas/tablas compatibles, backfill con jobs, feature toggle, luego contract sólo después de ventana de compatibilidad.
- En fail: parar rollout, recuperar versión compatible o restore aprobado, no intentar `migrate zero` destructivo automáticamente.
- Reinicio: audit que `.env` defaults no pisan cambios de GUI; test cuota MQTT no reset.

## DR y monitoreo
RPO/RTO son configurables según sector y operación; métricas disk/fill/TSDB compression, queue lag, gateway connectivity, failed command, data loss. No prometer alta disponibilidad si Compose single-host no está diseñado para ello.
