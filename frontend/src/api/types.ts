export interface Tenant {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  locale?: string;
}

export interface Unit {
  symbol: string;
  name: string;
  quantity: string;
}

export interface Project {
  id: string;
  tenant: string;
  name: string;
  code: string;
  lifecycle_status: string;
}

export interface Asset {
  id: string;
  tenant: string;
  project: string | null;
  name: string;
  external_ref: string;
  asset_type: string | null;
  parent: string | null;
  status: string;
  metadata: Record<string, unknown>;
}

export interface AssetTypeTemplateAttribute {
  code: string;
  name?: string;
  value_type: string;
  storage_datapoint?: boolean;
}

export interface AssetType {
  id: string;
  name: string;
  code: string;
  kind: "standard" | "gateway";
  description: string;
  schema: {
    attributes?: AssetTypeTemplateAttribute[];
  };
}

export interface AssetAttribute {
  id: string;
  asset: string;
  name: string;
  code: string;
  value_type: "string" | "boolean" | "number" | "json";
  unit: string | null;
  storage_datapoint: boolean;
  history_enabled: boolean;
  history_policy_override: Record<string, unknown> | null;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Me {
  id: string;
  email: string;
  full_name: string;
  is_platform_admin: boolean;
}

export interface Health {
  status: string;
  service: string;
  version: string;
  database: string;
}
