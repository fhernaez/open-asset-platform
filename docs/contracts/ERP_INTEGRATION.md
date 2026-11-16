# Integración ERP por requisición técnica

El ERP es autoridad sobre proveedores, compras/órdenes/facturas y estados comerciales; OAP administra activos, planes/órdenes de mantenimiento, stock técnico y una solicitud de abastecimiento ligada a work order.

## Contrato outbound
`RequisitionRequested(idempotency_key, tenant, project, work_order_id, part_id, sku, quantity, unit, required_by, requester)`; adapter ERP lo traduce al endpoint específico, guarda `external_requisition_id` y control de versión.

## Estado replicated inbound
`external_status=pending|approved|ordered|received|cancelled|failed`, timestamps, currency/cost references si permitido, firma webhook o poll y correlación. Rechazar transición inválida, impersonation, firma errónea, payload no versionado. La devolución de ERP no modifica stock sin movimiento autorizado o confirmación de recepción.

## Consistencia
Outbox + retries idempotentes, timeout, circuit breaker, DLQ y reconciliación por external_ref. Duplicado no crea dos requisiciones. Deshabilitar conector no invalida órdenes CMMS pendientes; muestra integración offline.
