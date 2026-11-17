import { http, HttpResponse } from "msw";

/**
 * Handlers por contrato (Fase 1: docs/contracts/openapi.yaml + OPENAPI_CONTRACTS.md).
 * Solo activos con VITE_ENABLE_MOCKS=true. Cada gate agrega aquí los handlers de
 * las pantallas que aún no tienen backend real, fieles a su contrato.
 */
export const handlers = [
  http.get("/api/v1/health", () =>
    HttpResponse.json({ status: "ok", service: "oap-api", version: "0.2.0", database: "up" }),
  ),
];
