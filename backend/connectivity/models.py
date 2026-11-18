"""Connectivity bounded context: gateways (as assets) and generic bindings.

A Gateway is the connectivity facet of an asset whose type is kind=gateway
(ADR-014): the asset holds identity/metadata, the Gateway holds protocol +
connection config (validated against the type's connection_schema) and the
bindings that route addresses (topics/registers) to attributes.
"""

from __future__ import annotations

from django.db import models

from platforms.models import TenantScopedModel


class Gateway(TenantScopedModel):
    asset = models.OneToOneField("assets.Asset", on_delete=models.CASCADE, related_name="gateway")
    protocol = models.CharField(max_length=32)
    config = models.JSONField(default=dict, blank=True)
    connection_status = models.CharField(
        max_length=16,
        choices=[("disconnected", "disconnected"), ("connected", "connected"), ("error", "error")],
        default="disconnected",
    )

    class Meta:
        db_table = "connectivity_gateway"

    def __str__(self) -> str:
        return f"{self.asset.name} ({self.protocol})"


class GatewayBinding(TenantScopedModel):
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE, related_name="bindings")
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE, related_name="connectivity_bindings")
    attribute = models.ForeignKey(
        "assets.AssetAttribute", on_delete=models.CASCADE, related_name="connectivity_bindings"
    )
    address = models.CharField(max_length=255)
    mapping = models.CharField(max_length=255, blank=True, default="")
    qos = models.IntegerField(default=0)
    polling = models.CharField(max_length=32, blank=True, default="")

    class Meta:
        db_table = "connectivity_gatewaybinding"
        unique_together = [("gateway", "attribute")]

    def __str__(self) -> str:
        return f"{self.gateway} -> {self.attribute.code}@{self.address}"
