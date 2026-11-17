"""Telemetry bounded context: current value, history, storage policies, metrics."""

from __future__ import annotations

from django.db import models

from core.models import UUIDPkModel


class StoragePolicy(UUIDPkModel):
    class OwnerType(models.TextChoices):
        AGENT = "agent"
        ATTRIBUTE = "attribute"

    owner_type = models.CharField(max_length=16, choices=OwnerType.choices)
    owner_id = models.UUIDField()
    version = models.IntegerField(default=1)
    enabled = models.BooleanField(default=True)
    mode = models.CharField(max_length=32, default="on_change")
    compare = models.JSONField(default=dict, blank=True)
    max_samples = models.JSONField(default=dict, blank=True)
    heartbeat = models.JSONField(default=dict, blank=True)
    window_type = models.CharField(max_length=16, default="fixed")
    late_event_policy = models.CharField(max_length=16, default="reject")
    invalid_quality = models.CharField(max_length=16, default="skip_history")
    changed_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    class Meta:
        db_table = "telemetry_storagepolicy"
        unique_together = [("owner_type", "owner_id", "version")]
        indexes = [models.Index(fields=["owner_type", "owner_id"])]

    def __str__(self) -> str:
        return f"{self.owner_type}:{self.owner_id} v{self.version}"


class StoragePolicyState(UUIDPkModel):
    """Durable per-attribute state so quota/baseline survive worker restarts."""

    attribute_id = models.UUIDField(unique=True)
    policy_version = models.IntegerField(default=1)
    last_persisted_value = models.JSONField(null=True, blank=True)
    last_persisted_ts = models.DateTimeField(null=True, blank=True)
    quota_bucket = models.BigIntegerField(null=True, blank=True)
    quota_count = models.IntegerField(default=0)
    watermark = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "telemetry_storagepolicystate"


class AttributeCurrent(models.Model):
    tenant_id = models.UUIDField(db_index=True)
    project_id = models.UUIDField(null=True, blank=True)
    asset_id = models.UUIDField()
    attribute_id = models.UUIDField(unique=True)
    observed_at = models.DateTimeField()
    value_type = models.CharField(max_length=16)
    typed_value = models.JSONField(null=True, blank=True)
    quality = models.CharField(max_length=16, default="good")
    source_event_id = models.CharField(max_length=200, blank=True, default="")
    ingest_time = models.DateTimeField(auto_now=True)
    version = models.BigIntegerField(default=1)

    class Meta:
        db_table = "telemetry_attributecurrent"


class TelemetryPoint(models.Model):
    tenant_id = models.UUIDField()
    attribute_id = models.UUIDField()
    ts = models.DateTimeField()
    ingested_at = models.DateTimeField()
    value_type = models.CharField(max_length=16)
    typed_value = models.JSONField(null=True, blank=True)
    quality = models.CharField(max_length=16, default="good")
    policy_version = models.IntegerField(default=1)
    source_event_id = models.CharField(max_length=200, blank=True, default="")
    dedupe_key = models.CharField(max_length=64)
    sequence = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "telemetry_telemetrypoint"
        indexes = [
            models.Index(fields=["attribute_id", "-ts"], name="telemetrypoint_attr_ts_idx"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["attribute_id", "dedupe_key"], name="uq_telemetrypoint_dedupe"),
        ]

    def __str__(self) -> str:
        return f"{self.attribute_id}@{self.ts.isoformat()}"


class IngestMetrics(models.Model):
    attribute_id = models.UUIDField()
    window_start = models.DateTimeField()
    received = models.BigIntegerField(default=0)
    valid = models.BigIntegerField(default=0)
    invalid = models.BigIntegerField(default=0)
    duplicate = models.BigIntegerField(default=0)
    accepted = models.BigIntegerField(default=0)
    filtered_equal = models.BigIntegerField(default=0)
    filtered_quota = models.BigIntegerField(default=0)
    late = models.BigIntegerField(default=0)
    failures = models.BigIntegerField(default=0)

    class Meta:
        db_table = "telemetry_ingestmetrics"
        unique_together = [("attribute_id", "window_start")]
