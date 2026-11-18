export interface OapRuntimeConfig {
  defaultLocale: string;
  defaultTimezone: string;
}

declare global {
  interface Window {
    __OAP_CONFIG__?: OapRuntimeConfig;
  }
}

/** Runtime configuration injected by the nginx container via /config.js (envsubst). */
export const RUNTIME: OapRuntimeConfig = {
  defaultLocale: window.__OAP_CONFIG__?.defaultLocale ?? "es",
  defaultTimezone: window.__OAP_CONFIG__?.defaultTimezone ?? "America/Argentina/Buenos_Aires",
};
