import { useQuery } from "@tanstack/react-query";
import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { listTenants } from "../api/endpoints";
import type { Tenant } from "../api/types";

interface AppContextValue {
  tenantId: string | undefined;
  projectId: string | undefined;
  tenant: Tenant | undefined;
  tenants: Tenant[];
  loading: boolean;
  setTenantId: (id: string | undefined) => void;
  setProjectId: (id: string | undefined) => void;
}

const AppContext = createContext<AppContextValue | null>(null);

function readStored(key: string): string | null {
  return localStorage.getItem(key);
}

function writeStored(key: string, value: string | undefined): void {
  if (value) {
    localStorage.setItem(key, value);
  } else {
    localStorage.removeItem(key);
  }
}

export function AppProvider({ children }: { children: React.ReactNode }) {
  const { i18n } = useTranslation();
  const [tenantId, setTenantIdState] = useState<string | undefined>(() => readStored("oap.tenant") ?? undefined);
  const [projectId, setProjectIdState] = useState<string | undefined>(
    () => readStored("oap.project") ?? undefined,
  );

  const tenantsQuery = useQuery({ queryKey: ["tenants"], queryFn: () => listTenants() });
  const tenants = useMemo(() => tenantsQuery.data?.results ?? [], [tenantsQuery.data]);

  // Auto-select the first organization when there is exactly one.
  useEffect(() => {
    if (!tenantId && tenants.length === 1) {
      setTenantIdState(tenants[0].id);
    }
  }, [tenantId, tenants]);

  const tenant = useMemo(
    () => tenants.find((t) => t.id === tenantId),
    [tenants, tenantId],
  );

  // Locale follows the selected organization (Tenant.locale).
  useEffect(() => {
    if (tenant?.locale && i18n.language !== tenant.locale) {
      void i18n.changeLanguage(tenant.locale);
    }
  }, [tenant, i18n]);

  function setTenantId(id: string | undefined) {
    setTenantIdState(id);
    writeStored("oap.tenant", id);
    if (!id) {
      setProjectId(undefined);
    }
  }

  function setProjectId(id: string | undefined) {
    setProjectIdState(id);
    writeStored("oap.project", id);
  }

  const value = useMemo<AppContextValue>(
    () => ({
      tenantId,
      projectId,
      tenant,
      tenants,
      loading: tenantsQuery.isLoading,
      setTenantId,
      setProjectId,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [tenantId, projectId, tenant, tenants, tenantsQuery.isLoading],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAppContext(): AppContextValue {
  const ctx = useContext(AppContext);
  if (!ctx) {
    throw new Error("useAppContext must be used within AppProvider");
  }
  return ctx;
}
