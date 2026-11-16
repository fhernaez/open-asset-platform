# Matriz de paridad — Atlas CMMS (objetivo, pendiente de auditoría completa)

| Área | Capacidades a auditar | OAP | Evidencia de paridad | Estado |
|---|---|---|---|---|
| Work orders | estados, asignaciones, prioridades, tiempos, checklist, adjuntos | CMMS | workflow+roles+history | TO_AUDIT |
| Preventive plans | por calendario/medidor/evento, recurrencia, generación | CMMS + Rules | pruebas de fecha/timezone/duplicado | TO_AUDIT |
| Work requests | solicitud, aprobación, rechazo, notificación | CMMS | UI + transiciones+audit | TO_AUDIT |
| Inventory | parts, almacenes, mínimo, movimientos, reservas | CMMS Inventory | invariantes stock+concurrencia | TO_AUDIT |
| Vendors | contactos, recursos, servicio, historial | CMMS | CRUD+auth+historial | TO_AUDIT |
| Procurement | compras/OC/aprobación en original | Integración ERP | requisición y estados externos | DIFFERENT_ARCHITECTURE |
| Analytics | compliance, downtime, costos, labor, reportes | CMMS Reports | cálculos fixture conocidos | TO_AUDIT |
| People | equipos, turnos, permisos, contratistas | Identity + CMMS | matrix permisos+assignment | TO_AUDIT |
| Notifications | email/webhook/eventos, recordatorios | Notifications | dedupe/retry/config | TO_AUDIT |
| Mobile | responsive/mobile workflow, offline si existe | React PWA | responsive/offline suite | TO_AUDIT |
| Fields/config | custom fields, workflows | CORE Schema + CMMS | update without migration | TO_AUDIT |
| Licencia comercial | identificar capacidades solo bajo comercial | implementación original | legal review + funcionalidad | TO_AUDIT |

No afirmar paridad de “todas las funcionalidades” hasta auditar y testear cada diferencia de la versión fijada.
