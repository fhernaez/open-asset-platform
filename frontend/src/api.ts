const API_BASE = import.meta.env.VITE_API_BASE ?? "/api/v1";

function token(): string | null {
  return localStorage.getItem("oap.access");
}

export function setToken(value: string | null) {
  if (value) {
    localStorage.setItem("oap.access", value);
  } else {
    localStorage.removeItem("oap.access");
  }
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string>),
  };
  const auth = token();
  if (auth) {
    headers.Authorization = `Bearer ${auth}`;
  }
  const response = await fetch(`${API_BASE}${path}`, { ...init, headers });
  if (response.status === 401) {
    setToken(null);
    throw new Error("unauthorized");
  }
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return (await response.json()) as T;
}

export async function login(email: string, password: string): Promise<void> {
  const data = await apiFetch<{ access: string; refresh: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  setToken(data.access);
}
