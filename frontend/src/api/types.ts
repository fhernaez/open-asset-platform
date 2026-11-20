export interface Tenant {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  locale?: string;
  timezone?: string;
}

export interface Unit {
  symbol: string;
  name: string;
  quantity: string;
}

export interface Gateway {
  id: string;
  asset: string;
  asset_name?: string;
  asset_code?: string;
  protocol: string;
  config: Record<string, unknown>;
  connection_status: string;
}

export interface GatewayBinding {
  id: string;
  gateway: string;
  asset: string;
  attribute: string;
  address: string;
  mapping: string;
  qos: number;
  polling: string;
}

export interface PluginSummary {
  slug: string;
  name: string;
  version: string;
  installed: boolean;
  enabled: boolean;
  effective: boolean;
  locked: boolean;
  is_core: boolean;
  health: string;
  dependencies: string[];
  permissions: string[];
}

export interface TelemetryCurrent {
  attribute_id: string;
  observed_at?: string;
  value_type?: string;
  value?: unknown;
  quality?: string;
  version?: number;
}

export interface TelemetryPoint {
  ts: string;
  value: unknown;
  value_type: string;
  quality: string;
  policy_version: number;
  source_event_id: string;
}

export interface TelemetryStats {
  attribute_id: string;
  totals: {
    received: number;
    accepted: number;
    filtered_equal: number;
    filtered_quota: number;
    invalid: number;
    duplicate: number;
    late: number;
  };
  samples: number;
}

export interface EffectivePolicy {
  attribute_id: string;
  history_enabled: boolean;
  storage_datapoint: boolean;
  source: string;
  mode: string;
  max_samples: { count: number | null; window: string | null };
  window_strategy: string | null;
  compare: Record<string, unknown>;
  policy_version: number | null;
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
  latitude?: number | null;
  longitude?: number | null;
  rel_x?: number | null;
  rel_y?: number | null;
  geofence?: Record<string, unknown> | null;
  image?: string | null;
  image_url?: string | null;
  designations?: Record<string, unknown>;
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
  auto_discovered?: boolean;
  is_active?: boolean;
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
  locale?: string;
  timezone?: string;
}

export interface Health {
  status: string;
  service: string;
  version: string;
  database: string;
}
