import { apiFetch } from "../api/client";
import type { Asset, AssetAttribute, Health, Paginated, Project, Tenant } from "../api/types";

export function health(): Promise<Health> {
  return apiFetch<Health>("/health");
}

export function listTenants(): Promise<Paginated<Tenant>> {
  return apiFetch<Paginated<Tenant>>("/platform/tenants/");
}

export function listProjects(tenantId: string): Promise<Paginated<Project>> {
  return apiFetch<Paginated<Project>>(`/platform/projects/?tenant=${tenantId}`);
}

export interface CreateAssetInput {
  tenant: string;
  project: string | null;
  name: string;
  external_ref: string;
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
