# Matriz de paridad — Atlas CMMS (auditada 2026-11-17, commit `06abfe35`)

Fuente fijada: `https://github.com/Grashjs/cmms` @ `06abfe35d09372ff80f889fcde73eb3cc71dc205`. Licencia dual: AGPL-3.0 (abierta) + Comercial (INTELLOOP LLC). Inventario por paths: `docs/research/GRAPH_SOURCE_INDEX.md`.

| Área | Capacidades verificadas en fuente (paths) | Estado | Destino OAP |
|---|---|---|---|
| Work orders | `controller/WorkOrderController.java` + Category/Configuration/History/MeterTrigger/RequestConfiguration; frontend `WorkOrders` | VERIFIED_SOURCE | OAP-CMM |
| Work requests | `controller/RequestController.java`, `RequestPortalController.java`; frontend `Requests` | VERIFIED_SOURCE | OAP-CMM |
| Preventive plans | `controller/PreventiveMaintenanceController.java`, `WorkOrderMeterTriggerController.java`; frontend `PreventiveMaintenance`, `Meters` | VERIFIED_SOURCE | OAP-CMM |
| Assets/equipos | `controller/AssetController.java`, `AssetCategoryController.java`, `AssetDowntimeController.java`; frontend `Assets`, `Categories` | VERIFIED_SOURCE | OAP-ASS + OAP-CMM |
| Inventory | `controller/PartController.java`, `PartCategoryController.java`, `PartQuantityController.java`, `MultiPartsController.java`; frontend `Inventory` | VERIFIED_SOURCE | OAP-CMM |
| Purchase orders | `controller/PurchaseOrderController.java` + Category; frontend `PurchaseOrders` | VERIFIED_SOURCE (OAP: requisición ERP, no submódulo de compras) | OAP-ERP + OAP-CMM |
| Meters/readings | `controller/MeterController.java`, `MeterCategoryController.java`, `ReadingController.java` | VERIFIED_SOURCE | OAP-CMM |
| Labor/tiempos | `controller/LaborController.java`, `TimeCategoryController.java`, `CostCategoryController.java`, `AdditionalCostController.java` | VERIFIED_SOURCE | OAP-CMM |
| Checklist | `controller/ChecklistController.java` | VERIFIED_SOURCE | OAP-CMM |
| Teams/people | `controller/TeamController.java`, `UserController.java`, `RoleController.java`, `ShiftConfigurationController.java`, `ScheduleController.java`; frontend `PeopleAndTeams` | VERIFIED_SOURCE | OAP-CMM + OAP-PLT |
| Vendors/customers | `controller/VendorController.java`, `CustomerController.java`; frontend `VendorsAndCustomers` | VERIFIED_SOURCE | OAP-CMM |
| Locations | `controller/LocationController.java`, `FloorPlanController.java` (planos de planta); frontend `Locations` | VERIFIED_SOURCE | OAP-GIS + OAP-CMM |
| Files/adjuntos | `controller/FileController.java` (MinIO/GCP); frontend `Files` | VERIFIED_SOURCE | OAP-CMM |
| Analytics | `controller/analytics/`: AssetAnalytics, PartAnalytics, RequestAnalytics, UserAnalytics, WOAnalytics; frontend `Analytics` | VERIFIED_SOURCE | OAP-CMM |
| Notifications/webhooks | `controller/NotificationController.java`, `WebhookController.java`, `WebhookEndpointController.java` | VERIFIED_SOURCE | OAP-PLT + OAP-CMM |
| Workflows | `controller/WorkflowController.java`, `WorkOrderConfigurationController.java` | VERIFIED_SOURCE | OAP-CMM |
| Custom fields | `controller/CustomFieldController.java`, `FieldConfigurationController.java`, `UiConfigurationController.java`, `model/CustomField.java` | VERIFIED_SOURCE | OAP-CMM |
| Import/export | `controller/ImportController.java`, `ExportController.java`; frontend `Imports` | VERIFIED_SOURCE | OAP-CMM |
| Mobile | `mobile/` (React Native, apps en stores) | VERIFIED_SOURCE | OAP-CMM (PWA responsive P2) |
| i18n | 16 idiomas listados en README | VERIFIED_SOURCE | OAP-PLT (es/en base, P2 resto) |
| White labeling / branding | `LICENSE_KEY`, `LOGO_PATHS`, `BRAND_CONFIG`, `CUSTOM_COLORS` ("Needs a license") | COMMERCIAL_UNAVAILABLE | OAP-CMM (implementación original opcional) |
| SSO / LDAP | `ENABLE_SSO`, `OAUTH2_*`, `LDAP_ENABLED` + `LicenseService.isSSOEnabled()` | COMMERCIAL_UNAVAILABLE | OAP-PLT (OIDC original, futuro) |
| Enterprise features | `LicenseService.hasEntitlement(LicenseEntitlement)`; Feature Matrix en pricing | COMMERCIAL_UNAVAILABLE | no copiar; diseñar original si aplica |
| Integration con telemetría MQTT/on_change N-T | no presente (Atlas no ingiere telemetría IoT) | NEW_REQUIREMENT | OAP-TEL + OAP-MQT |
| Integración con OpenRemote (assets compartidos con telemetría) | no presente | NEW_REQUIREMENT | OAP-ASS ↔ OAP-TEL |

Regla: OAP implementa capacidades equivalentes con diseño propio (sin copiar código AGPLv3 ni features comerciales); cada fila se cierra con contrato + código + test + evidencia en `TRACEABILITY.md`.
