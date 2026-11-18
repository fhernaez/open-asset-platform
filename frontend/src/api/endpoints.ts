import { apiFetch } from "../api/client";
import type {
  Asset,
  AssetAttribute,
  AssetType,
  EffectivePolicy,
  Gateway,
  GatewayBinding,
  Health,
  Paginated,
  PluginSummary,
  Project,
  TelemetryCurrent,
  TelemetryPoint,
  TelemetryStats,
  Tenant,
  Unit,
} from "../api/types";

export function health(): Promise<Health> {
  return apiFetch<Health>("/health");
}

export function listTenants(): Promise<Paginated<Tenant>> {
  return apiFetch<Paginated<Tenant>>("/platform/tenants/");
}

export function createTenant(input: { name: string; slug: string }): Promise<Tenant> {
  return apiFetch<Tenant>("/platform/tenants/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function listProjects(tenantId: string): Promise<Paginated<Project>> {
  return apiFetch<Paginated<Project>>(`/platform/projects/?tenant=${tenantId}`);
}

export function createProject(input: { tenant: string; name: string; code: string }): Promise<Project> {
  return apiFetch<Project>("/platform/projects/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export interface CreateAssetInput {
  tenant: string;
  project: string | null;
  name: string;
  external_ref: string;
  asset_type?: string | null;
  gateway_config?: Record<string, unknown>;
}

export interface CreateAssetTypeInput {
  tenant: string;
  name: string;
  code: string;
  kind: "standard" | "gateway";
  description?: string;
  schema: { attributes?: { code: string; name?: string; value_type: string; storage_datapoint?: boolean }[] };
}

export function listAssetTypes(params: { tenant?: string; kind?: string } = {}): Promise<Paginated<AssetType>> {
  const query = new URLSearchParams();
  if (params.tenant) query.set("tenant", params.tenant);
  if (params.kind) query.set("kind", params.kind);
  const qs = query.toString();
  return apiFetch<Paginated<AssetType>>(`/assets/types/${qs ? `?${qs}` : ""}`);
}

export function createAssetType(input: CreateAssetTypeInput): Promise<AssetType> {
  return apiFetch<AssetType>("/assets/types/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function listAssets(params: { tenant?: string; project?: string } = {}): Promise<Paginated<Asset>> {
  const query = new URLSearchParams();
  if (params.tenant) query.set("tenant", params.tenant);
  if (params.project) query.set("project", params.project);
  const qs = query.toString();
  return apiFetch<Paginated<Asset>>(`/assets/assets/${qs ? `?${qs}` : ""}`);
}

export function createAsset(input: CreateAssetInput): Promise<Asset> {
  return apiFetch<Asset>("/assets/assets/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function listAttributes(assetId: string): Promise<Paginated<AssetAttribute>> {
  return apiFetch<Paginated<AssetAttribute>>(`/assets/attributes/?asset=${assetId}`);
}

export interface CreateAttributeInput {
  asset: string;
  name: string;
  code: string;
  value_type: string;
  storage_datapoint: boolean;
}

export function createAttribute(input: CreateAttributeInput): Promise<AssetAttribute> {
  return apiFetch<AssetAttribute>("/assets/attributes/", {
    method: "POST",
    body: JSON.stringify({ ...input, history_enabled: input.storage_datapoint }),
  });
}

export function updateAssetStatus(id: string, status: string): Promise<Asset> {
  return apiFetch<Asset>(`/assets/assets/${id}/`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}

export function deleteAsset(id: string): Promise<void> {
  return apiFetch<void>(`/assets/assets/${id}/`, { method: "DELETE" });
}

export function deleteAssetType(id: string): Promise<void> {
  return apiFetch<void>(`/assets/types/${id}/`, { method: "DELETE" });
}

export function updateAttribute(
  id: string,
  input: Partial<Pick<AssetAttribute, "name" | "code" | "value_type" | "unit" | "storage_datapoint">>,
): Promise<AssetAttribute> {
  return apiFetch<AssetAttribute>(`/assets/attributes/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export function deleteAttribute(id: string): Promise<void> {
  return apiFetch<void>(`/assets/attributes/${id}/`, { method: "DELETE" });
}

export function listUnits(): Promise<Paginated<Unit>> {
  return apiFetch<Paginated<Unit>>("/assets/units/");
}

// --- Connectivity ----------------------------------------------------------

export function listGateways(params: { tenant?: string; protocol?: string } = {}): Promise<Paginated<Gateway>> {
  const query = new URLSearchParams();
  if (params.tenant) query.set("tenant", params.tenant);
  if (params.protocol) query.set("protocol", params.protocol);
  const qs = query.toString();
  return apiFetch<Paginated<Gateway>>(`/connectivity/gateways/${qs ? `?${qs}` : ""}`);
}

export function createGateway(input: {
  tenant: string;
  project: string | null;
  asset: string;
  protocol: string;
  config: Record<string, unknown>;
}): Promise<Gateway> {
  return apiFetch<Gateway>("/connectivity/gateways/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function updateGatewayConfig(id: string, config: Record<string, unknown>): Promise<Gateway> {
  return apiFetch<Gateway>(`/connectivity/gateways/${id}/`, {
    method: "PATCH",
    body: JSON.stringify({ config }),
  });
}

export function deleteGateway(id: string): Promise<void> {
  return apiFetch<void>(`/connectivity/gateways/${id}/`, { method: "DELETE" });
}

export function listBindings(gatewayId: string): Promise<Paginated<GatewayBinding>> {
  return apiFetch<Paginated<GatewayBinding>>(`/connectivity/bindings/?gateway=${gatewayId}`);
}

export function createBinding(input: {
  gateway: string;
  asset: string;
  attribute: string;
  address: string;
  mapping?: string;
  qos?: number;
}): Promise<GatewayBinding> {
  return apiFetch<GatewayBinding>("/connectivity/bindings/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function deleteBinding(id: string): Promise<void> {
  return apiFetch<void>(`/connectivity/bindings/${id}/`, { method: "DELETE" });
}

export function gatewayStoragePolicy(
  id: string,
  policy?: Record<string, unknown>,
): Promise<{ gateway_id: string; storage_policy: Record<string, unknown> }> {
  if (policy) {
    return apiFetch(`/connectivity/gateways/${id}/storage-policy/`, {
      method: "PUT",
      body: JSON.stringify({ storage_policy: policy }),
    });
  }
  return apiFetch(`/connectivity/gateways/${id}/storage-policy/`);
}

// --- Telemetry -------------------------------------------------------------

export function telemetryCurrent(attributeId: string): Promise<TelemetryCurrent> {
  return apiFetch<TelemetryCurrent>(`/telemetry/attributes/${attributeId}/current/`);
}

export function telemetryHistory(attributeId: string, from?: string, to?: string): Promise<{ attribute_id: string; points: TelemetryPoint[] }> {
  const query = new URLSearchParams();
  if (from) query.set("from", from);
  if (to) query.set("to", to);
  const qs = query.toString();
  return apiFetch(`/telemetry/attributes/${attributeId}/history/${qs ? `?${qs}` : ""}`);
}

export function telemetryStats(attributeId: string): Promise<TelemetryStats> {
  return apiFetch<TelemetryStats>(`/telemetry/attributes/${attributeId}/stats/`);
}

export function effectivePolicy(attributeId: string, gatewayId?: string): Promise<EffectivePolicy> {
  const query = gatewayId ? `?gateway=${gatewayId}` : "";
  return apiFetch<EffectivePolicy>(`/telemetry/attributes/${attributeId}/policy/effective/${query}`);
}

// --- Plugins ---------------------------------------------------------------

export function listPlugins(): Promise<PluginSummary[]> {
  return apiFetch<PluginSummary[]>("/plugins/");
}

export function setPluginEnabled(
  slug: string,
  enabled: boolean,
): Promise<{ slug: string; enabled: boolean; effective: boolean; locked: boolean }> {
  return apiFetch(`/plugins/${slug}/activation/`, {
    method: "PATCH",
    body: JSON.stringify({ enabled }),
  });
}
