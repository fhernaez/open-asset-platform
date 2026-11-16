from django.contrib import admin

from telemetry.models import (
    AttributeCurrent,
    IngestMetrics,
    StoragePolicy,
    StoragePolicyState,
    TelemetryPoint,
)


@admin.register(StoragePolicy)
class StoragePolicyAdmin(admin.ModelAdmin):
    list_display = ["owner_type", "owner_id", "version", "mode", "enabled"]


@admin.register(StoragePolicyState)
class StoragePolicyStateAdmin(admin.ModelAdmin):
    list_display = ["attribute_id", "policy_version", "quota_bucket", "quota_count"]


@admin.register(AttributeCurrent)
class AttributeCurrentAdmin(admin.ModelAdmin):
    list_display = ["attribute_id", "asset_id", "value_type", "quality", "observed_at"]


@admin.register(TelemetryPoint)
class TelemetryPointAdmin(admin.ModelAdmin):
    list_display = ["attribute_id", "ts", "value_type", "quality", "source_event_id"]


@admin.register(IngestMetrics)
class IngestMetricsAdmin(admin.ModelAdmin):
    list_display = ["attribute_id", "window_start", "received", "accepted", "filtered_equal", "filtered_quota"]
