"""MQTT plugin bounded context: brokers, agents, bindings, discovery, health."""

from __future__ import annotations

from django.db import models

from platforms.models import TenantScopedModel


class BrokerConnection(TenantScopedModel):
    name = models.CharField(max_length=160)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=1883)
    tls = models.BooleanField(default=False)
    credentials_secret_ref = models.CharField(max_length=255, blank=True, default="")
    client_id = models.CharField(max_length=120, blank=True, default="")
    acl_scope = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "mqtt_brokerconnection"

    def __str__(self) -> str:
        return f"{self.name} ({self.host}:{self.port})"


class MqttAgent(TenantScopedModel):
    name = models.CharField(max_length=160)
    broker = models.ForeignKey(BrokerConnection, on_delete=models.PROTECT, related_name="agents")
    client_id = models.CharField(max_length=120, blank=True, default="")
    subscription_defs = models.JSONField(default=list, blank=True)
    storage_policy_defaults = models.JSONField(default=dict, blank=True)
    connection_status = models.CharField(
        max_length=16,
        choices=[("disconnected", "disconnected"), ("connected", "connected"), ("error", "error")],
        default="disconnected",
    )

    class Meta:
        db_table = "mqtt_mqttagent"

    def __str__(self) -> str:
        return self.name


class MqttBinding(TenantScopedModel):
    agent = models.ForeignKey(MqttAgent, on_delete=models.CASCADE, related_name="bindings")
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE, related_name="mqtt_bindings")
    attribute = models.ForeignKey("assets.AssetAttribute", on_delete=models.CASCADE, related_name="mqtt_bindings")
    subscribe_topic = models.CharField(max_length=255)
    publish_topic = models.CharField(max_length=255, blank=True, default="")
    json_path = models.CharField(max_length=255, blank=True, default="")
    qos = models.IntegerField(default=0)
    retain_policy = models.CharField(max_length=16, default="ignore")

    class Meta:
        db_table = "mqtt_mqttbinding"
        unique_together = [("agent", "attribute")]


class MqttDiscoveryTemplate(TenantScopedModel):
    name = models.CharField(max_length=160)
    topic_pattern = models.CharField(max_length=255)
    device_id_mapping = models.JSONField(default=dict, blank=True)
    attribute_schema = models.JSONField(default=dict, blank=True)
    approval_required = models.BooleanField(default=True)

    class Meta:
        db_table = "mqtt_mqttdiscoverytemplate"


class MqttSubscriptionHealth(models.Model):
    agent = models.ForeignKey(MqttAgent, on_delete=models.CASCADE, related_name="health")
    connectivity = models.CharField(max_length=16, default="unknown")
    received = models.BigIntegerField(default=0)
    published = models.BigIntegerField(default=0)
    backpressure = models.BigIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mqtt_mqttsubscriptionhealth"
