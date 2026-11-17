# CORE / Edge Provisioning

## Objetivo de producto y límites de propiedad
Provisionar gateways y devices, credentials/rotation, sincronización offline de atributos/eventos y reconciliación de conflictos.

## Entidades y campos propuestos (Django models; ajustar con ADR si cambia)
- `Gateway(id, tenant, project, certificate_ref, status)`.
- `DeviceEnrollment(token_hash, expiry, used)`.
- `EdgeCheckpoint(gateway, seq, last_sync)`.
- `EdgeSpoolManifest(gateway, partition, size, checksum)`.

## Endpoints propuestos — `/api/v1/`, documentación OpenAPI, RBAC y errores uniformes
- `POST /api/v1/gateways:enroll`.
- `GET/POST /api/v1/gateways/{id}/sync`.
- `POST /api/v1/gateways/{id}:revoke`.

## Invariantes funcionales / reglas de negocio
- Gateway no adquiere tenant por autodiscovery no autenticado.
- Rotación credenciales y ACL broker por gateway.
- Spool con cuotas, orden y dedupe, nunca RAM infinita.
- Conflictos de write comando se rechazan; lecturas tardías llevan calidad/ts.

## Flujo de implementación mínimo
1. Crear migraciones propias sin tocar tablas privadas de otro módulo; índices/unique constraints por tenant y proyecto cuando aplique.
2. Exponer servicios de dominio transaccionales; emitir eventos outbox versionados en los cambios relevantes.
3. Añadir serializers/DRF endpoints con permisos por objeto, filtros, paginación, errores y OpenAPI.
4. Añadir UI React de este flujo con loading/error/empty/disabled states y traducción ES/EN; no usar admin Django como único frontend definitivo.
5. Crear tests unitarios (invariantes), integración PostgreSQL/PostGIS cuando corresponda y E2E para acciones visibles.
6. Releer `docs/architecture/MASTER_ARCHITECTURE.md` y contratos relacionados; adjuntar evidencia al gate sin falsas afirmaciones.

## Tests contractuales y de aceptación obligatorios
- [ ] Gateway desconectado cachea N eventos y luego replay no duplica.
- [ ] Revoked cert no publica/consume.
- [ ] Spool limit alcanzado crea métrica/alarma.
- [ ] Upgrade edge conserva checkpoint o resync explícito.

## Casos negativos comunes
- Actor sin permisos -> respuesta 403 o 404 que no expone existencia de objeto de otro tenant.
- Payload inválido -> 400/422 sin modificación parcial ni 500; JSON Schema/serializer valida.
- Retries concurrentes -> idempotencia o conflicto 409, nunca registros duplicados.
- Restart API/worker -> conservar datos/configuración y reanudar operaciones con observabilidad.

## Dependencias y compatibilidad
Contratos públicos versionados (`docs/contracts/*`), auditoría, identidad, eventos, despliegue Docker y documentación del gate. Prohibido importar código de plugins desde CORE. Los detalles se implementan gradualmente sin usar stubs como sustituto de acceptance.
