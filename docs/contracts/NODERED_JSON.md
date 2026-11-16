# Node-RED JSON bidireccional, modelo de negociación y export de pestaña

## Import
Aceptar JSON de selección de nodos y exportación flow/flows según formato detectado; no asumir estructura única. Parsear node types `tab`, `mqtt in`, `mqtt out`, `mqtt-broker`, `function`, `change`, `json`, y wiring arrays. Extraer topics, broker config, JSONPath/mapping inferible, tags. Para function JavaScript o topics dinámicos: generar `unresolved` y requerir confirmación humana; nunca ejecutar JS importado durante parse.

## Preview → Commit
`FlowImportProposal` con original_checksum, source_instance, tabs, devices, points, maps, unresolved, dangerous_writes; asignar tenant/project, dedupe por external refs, dry-run. Commit transaccional, auditado e idempotente; si cambia JSON tras preview, exigir nuevo checksum.

## Export
Seleccionar asset o grupo, generar tab + nodes con `oap_asset_id` estable en metadata y nombres descriptivos, subscriptions/publications declarativos, referencias a credenciales/hosts via config placeholders. Validación de importabilidad JSON de Node-RED y de subset de nodos. Nunca incluir passwords, tokens, detalles de autorización. `FlowMapping` guarda ID tab/flow remoto y hash; actualizar con compare-and-swap para no pisar edición humana.

## Disparar procesos
Eventos de dominio → webhook HTTP In autenticado o MQTT topic firmado/ACL → Node-RED; no usar `POST /flow` como operación de ejecución. Errores con retries acotados, result/audit visible. Node-RED opcional: OAP ingestion, sampling, reglas y dashboards siguen operando si se elimina por completo.

## Pruebas
Export de OAP se importa sin errores en instancia Node-RED de test y crea una única pestaña. Import de flow importado genera assets/points esperados, reimport no duplica. Flow cambiado manualmente → 409/conflict. Sin Node-RED no falla health core ni MQTT directo. JSON malicioso/función no se ejecuta.
