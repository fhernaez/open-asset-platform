"""Asset registry bounded context: assets, typed attributes, relationships."""

from __future__ import annotations

from django.db import models

from platforms.models import TenantScopedModel


class Unit(models.Model):
    symbol = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=80)
    quantity = models.CharField(max_length=40, blank=True, default="")

    class Meta:
        db_table = "assets_unit"

    def __str__(self) -> str:
        return self.symbol


class AssetType(TenantScopedModel):
    class Kind(models.TextChoices):
        STANDARD = "standard"
        GATEWAY = "gateway"

    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=80)
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.STANDARD)
    is_location = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    schema = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "assets_assettype"
        unique_together = [("tenant", "code")]

    def __str__(self) -> str:
        return self.code


class Asset(TenantScopedModel):
    class Status(models.TextChoices):
        DRAFT = "draft"
        ACTIVE = "active"
        RETIRED = "retired"

    name = models.CharField(max_length=200)
    external_ref = models.CharField(max_length=200, blank=True, default="")
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True, blank=True, related_name="assets")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    metadata = models.JSONField(default=dict, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # Location inheritance (ADR-017): relative to the nearest location-ancestor image.
    rel_x = models.FloatField(null=True, blank=True)
    rel_y = models.FloatField(null=True, blank=True)
    # GeoJSON polygon (location assets) drawn on the global map.
    geofence = models.JSONField(null=True, blank=True)
    # Own image (location assets), uploaded to media/.
    image = models.ImageField(upload_to="locations", null=True, blank=True, max_length=255)
    # IEC/ISO 81346 designations, versioned per aspect (ADR-018):
    # {aspect: {code, occurrence}, "version": n, "history": [...]}
    designations = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "assets_asset"
        unique_together = [("tenant", "external_ref")]
        ordering = ["name"]
        indexes = [models.Index(fields=["tenant_id", "project_id", "id"])]

    def __str__(self) -> str:
        return self.name


class AssetAttribute(TenantScopedModel):
    class ValueType(models.TextChoices):
        STRING = "string"
        BOOLEAN = "boolean"
        NUMBER = "number"
        JSON = "json"

    class Quality(models.TextChoices):
        GOOD = "good"
        STALE = "stale"
        INVALID = "invalid"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="attributes")
    name = models.CharField(max_length=160)
    code = models.SlugField(max_length=120)
    value_type = models.CharField(max_length=16, choices=ValueType.choices, default=ValueType.NUMBER)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    description = models.TextField(blank=True, default="")
    # Telemetry / storage policy (public fields; effective policy is in telemetry).
    storage_datapoint = models.BooleanField(default=False)
    history_enabled = models.BooleanField(default=False)
    history_policy_override = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    # Auto-discovery (ADR-014 v2): candidates extracted from gateway payloads.
    auto_discovered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "assets_assetattribute"
        unique_together = [("asset", "code")]
        indexes = [models.Index(fields=["asset_id", "id"])]

    def __str__(self) -> str:
        return f"{self.asset.name}.{self.code}"


class AssetRelationship(models.Model):
    tenant = models.ForeignKey("platforms.Tenant", on_delete=models.CASCADE, related_name="+")
    source = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="outgoing")
    target = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="incoming")
    relation_type = models.CharField(max_length=80)

    class Meta:
        db_table = "assets_assetrelationship"
        unique_together = [("source", "target", "relation_type")]
