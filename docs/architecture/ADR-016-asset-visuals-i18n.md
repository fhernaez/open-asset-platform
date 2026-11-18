# ADR: Representación visual de activos e i18n estructural

Estado: **Aceptada** (2026-11-18).

## Contexto

La representación gráfica de los activos es estructural: será central en dashboards, paneles de operación, planos y mapas. Las referencias auditadas (OpenRemote `ui/component/or-icon`, iconos/imagen de entidad de ThingsBoard, iconos de nodos de Node-RED) muestran tres capas visuales: icono por tipo, imagen por entidad y color por estado. Además el producto será multilenguaje: la UI, la administración y los tipos creados por la comunidad deben poder traducirse, sin traducir datos del usuario.

## Decisión

1. **Modelo visual de 3 capas** para activos (ver `docs/contracts/ASSET_TYPE_SCHEMA.md`):
   - `icon` por **tipología** (librería SVG integrada + subida custom por tenant, P2).
   - `image` opcional por **activo** (foto/símbolo, para planos/mapas/dashboards).
   - Rendering de **estado** derivado (color/badge por status/alarma) para overlays.
2. **i18n estructural:**
   - UI con react-i18next + locales de Ant Design; idiomas base **es/en**.
   - **Resolución de locale**: `User.locale` (si está definido) → `Tenant.locale` → **`OAP_DEFAULT_LOCALE`** (variable de entorno del SERVICIO frontend; default `es`). El contenedor nginx genera `/config.js` con `window.__OAP_CONFIG__` vía envsubst en el arranque y el bundle lo lee antes de inicializar i18n.
   - **Resolución de timezone** (formateo de timestamps en UI; el backend sigue en UTC): `User.timezone` → `Tenant.timezone` → `OAP_DEFAULT_TIMEZONE` (default `America/Argentina/Buenos_Aires`).
   - Manifiestos de tipología (y catálogo semilla) declaran `label_i18n`/`description_i18n` (mínimo es/en); los schemas de conexión también (`label_i18n` por campo).
   - Los datos de usuario (nombres de activos, proyectos, org) NO se traducen.
3. **Convergencia con el editor visual:** el futuro editor gráfico de tipologías (G9) genera el MISMO `ASSET_TYPE_SCHEMA`; no existe segundo formato. La comunidad puede aportar tipos por manifiestos de código o, a futuro, por export/import de bundles.

## Consecuencias

- `AssetType.schema` pasa a ser el manifiesto completo validado (attributes + connection_schema + icon + i18n); el `name` legacy se mantiene como alias del locale primario.
- Las pantallas renderizan iconos y colores de estado; las tablas/árbol muestran `label_i18n` según locale activo.
- El catálogo semilla (~22 tipos) incluye iconos y etiquetas es/en desde el seed.

## Alternativas consideradas

- Solo icono sin imagen/estado: insuficiente para planos/dashboards (rechazado).
- i18n solo de UI sin manifiestos traducibles: bloquea tipos comunitarios multilingües (rechazado).
- Traducir datos de usuario: rechazado (datos ≠ UI).
