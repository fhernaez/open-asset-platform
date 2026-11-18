export interface ApiErrorBody {
  type?: string;
  title?: string;
  status?: number;
  detail?: string;
}

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api/v1";

let authToken: string | null = localStorage.getItem("oap.access");
let onUnauthorized: (() => void) | null = null;

export function setAuthToken(token: string | null): void {
  authToken = token;
  if (token) {
    localStorage.setItem("oap.access", token);
  } else {
    localStorage.removeItem("oap.access");
  }
}

export function setUnauthorizedHandler(handler: () => void): void {
  onUnauthorized = handler;
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...(init.headers as Record<string, string>),
  };
  if (init.body) {
    headers["Content-Type"] = "application/json";
  }
  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  }
  const response = await fetch(`${API_BASE}${path}`, { ...init, headers });
  if (response.status === 401) {
    setAuthToken(null);
    onUnauthorized?.();
    throw new ApiError(401, "Session expired.");
  }
  if (!response.ok) {
    let detail = `HTTP ${response.status}`;
    try {
      const body = (await response.json()) as ApiErrorBody;
      detail = body.detail ?? JSON.stringify(body);
    } catch {
      // keep generic detail
    }
    throw new ApiError(response.status, detail);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  const text = await response.text();
  if (!text) {
    return undefined as T;
  }
  return JSON.parse(text) as T;
}

export function get(path: string): Promise<unknown> {
  return apiFetch(path);
}
