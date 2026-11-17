# Política de licencias FOSS, ingeniería limpia y publicación GitHub

El usuario quiere un repositorio público realmente FOSS y prestaciones sin activaciones de pago. Esto **no** permite suprimir notices AGPL, copiar módulos solo comerciales ni eliminar limitaciones técnicas/licencias del proveedor. Se desarrollarán implementaciones propias de funciones documentadas externamente; para código reutilizado exigir licencia, atribución y cumplimiento AGPLv3 cuando aplique.

## Auditoría obligatoria
- Para cada dependencia: nombre, versión, SPDX, licencia de código y de datos/modelos, origen, hash, uso backend/frontend/contenedor, NOTICE.
- Revisar dual licensing Atlas y distinción entre código abierto disponible y capacidades no publicadas. Un `LICENSE_KEY` en fuente no habilita automáticamente a reutilizar todo código comercial.
- OpenRemote: verificar licencia, partes, asset bundles, marcas y atribuciones.
- Extensiones PostgreSQL (PostGIS): revisar licencia aplicable a la extensión y funcionalidades efectivamente incluidas; no usar funciones bajo licencia incompatible con el objetivo FOSS.
- MapLibre, tiles, GIS, iconos, imágenes y mapas Google/OSM, LLM local y pesos: licencias diferentes. No empaquetar bases cartográficas fuera de términos autorizados.
- IEC/ISO 81346: implementar conceptos sin redistribuir texto pagado de normas. Revisar normas exactas y ediciones.

## Entregables previos a release
`LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES`, SPDX SBOM (CycloneDX o SPDX), política de contribución, SECURITY.md, DCO o CLA según decisión legal, matriz de uso de marcas, registro de la auditoría.

## Gate
Si un componente no tiene licencia verificable o compatibilidad aprobada, mantenerlo fuera del paquete público y reportar bloqueo. No esconderlo detrás de un plugin.
