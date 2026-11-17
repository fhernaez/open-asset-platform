export type Gate = "G2" | "G3" | "G4" | "G5" | "G6" | "G7" | "G8" | "G9";

export interface ScreenFlag {
  key: string;
  label: string;
  gate: Gate;
}

export const SCREENS: ScreenFlag[] = [
  { key: "assets", label: "Activos", gate: "G2" },
  { key: "telemetry", label: "Telemetría", gate: "G4" },
  { key: "mqtt", label: "MQTT", gate: "G4" },
  { key: "plugins", label: "Plugins", gate: "G3" },
  { key: "dashboards", label: "Dashboards", gate: "G6" },
  { key: "gis", label: "Mapas/GIS", gate: "G6" },
  { key: "rules", label: "Reglas", gate: "G7" },
  { key: "cmms", label: "CMMS", gate: "G5" },
  { key: "nodered", label: "Node-RED", gate: "G8" },
  { key: "ai", label: "IA/MCP", gate: "G8" },
  { key: "admin", label: "Administración", gate: "G3" },
];

/**
 * Feature flags per gate. A screen whose implementation has not landed must
 * never render broken controls: it shows a "disponible en etapa X" notice.
 * Add a screen to IMPLEMENTED_SCREENS only when its backend wiring is real.
 */
export const IMPLEMENTED_SCREENS: Set<string> = new Set(["assets"]);

export function isScreenImplemented(key: string): boolean {
  return IMPLEMENTED_SCREENS.has(key);
}
