export type Gate = "G2" | "G3" | "G4" | "G5" | "G6" | "G7" | "G8" | "G9";

export interface ScreenFlag {
  key: string;
  labelKey: string;
  gate: Gate;
}

/**
 * Menú canónico — definido en docs/architecture/MASTER_ARCHITECTURE.md §9.1 y
 * ADR-014. Cualquier cambio de secciones debe actualizarse primero en esos
 * documentos y luego replicarse aquí. Labels resueltos por i18n (labelKey).
 */
export const SCREENS: ScreenFlag[] = [
  { key: "assets", labelKey: "menu.assets", gate: "G2" },
  { key: "connectivity", labelKey: "menu.connectivity", gate: "G4" },
  { key: "telemetry", labelKey: "menu.telemetry", gate: "G4" },
  { key: "dashboards", labelKey: "menu.dashboards", gate: "G6" },
  { key: "maps", labelKey: "menu.maps", gate: "G6" },
  { key: "rules", labelKey: "menu.rules", gate: "G7" },
  { key: "cmms", labelKey: "menu.cmms", gate: "G5" },
  { key: "integrations", labelKey: "menu.integrations", gate: "G8" },
  { key: "ai", labelKey: "menu.ai", gate: "G8" },
  { key: "admin", labelKey: "menu.admin", gate: "G3" },
];

/**
 * Feature flags per gate. A screen whose implementation has not landed must
 * never render broken controls: it shows a "disponible en etapa X" notice.
 * Add a screen to IMPLEMENTED_SCREENS only when its backend wiring is real.
 */
export const IMPLEMENTED_SCREENS: Set<string> = new Set([
  "assets",
  "connectivity",
  "telemetry",
  "plugins",
  "dashboards",
  "maps",
  "admin",
]);

export function isScreenImplemented(key: string): boolean {
  return IMPLEMENTED_SCREENS.has(key);
}
