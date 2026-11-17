import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { apiFetch, setAuthToken, setUnauthorizedHandler } from "../api/client";
import type { Me } from "../api/types";

interface AuthContextValue {
  user: Me | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface LoginResponse {
  access: string;
  refresh: string;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Me | null>(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem("oap.access")));

  const logout = useCallback(() => {
    setAuthToken(null);
    setUser(null);
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(logout);
  }, [logout]);

  useEffect(() => {
    if (!localStorage.getItem("oap.access")) {
      setLoading(false);
      return;
    }
    apiFetch<Me>("/auth/me")
      .then(setUser)
      .catch(() => logout())
      .finally(() => setLoading(false));
  }, [logout]);

  const login = useCallback(async (email: string, password: string) => {
    const data = await apiFetch<LoginResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setAuthToken(data.access);
    const me = await apiFetch<Me>("/auth/me");
    setUser(me);
  }, []);

  const value = useMemo(() => ({ user, loading, login, logout }), [user, loading, login, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
