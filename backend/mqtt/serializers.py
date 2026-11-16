from __future__ import annotations

from rest_framework import serializers

from mqtt.models import (
    BrokerConnection,
    MqttAgent,
    MqttBinding,
    MqttDiscoveryTemplate,
    MqttSubscriptionHealth,
)


class BrokerConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerConnection
        fields = [
            "id",
            "tenant",
            "project",
            "name",
            "host",
            "port",
            "tls",
            "credentials_secret_ref",
            "client_id",
            "acl_scope",
        ]
        read_only_fields = ["tenant", "project"]


class MqttAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MqttAgent
        fields = [
            "id",
            "tenant",
            "project",
            "name",
            "broker",
            "client_id",
            "subscription_defs",
            "storage_policy_defaults",
            "connection_status",
        ]
        read_only_fields = ["tenant", "project", "connection_status"]


class MqttBindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MqttBinding
        fields = [
            "id",
            "tenant",
            "project",
            "agent",
            "asset",
            "attribute",
            "subscribe_topic",
            "publish_topic",
            "json_path",
            "qos",
            "retain_policy",
        ]
        read_only_fields = ["tenant", "project"]


class MqttDiscoveryTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MqttDiscoveryTemplate
        fields = [
            "id",
            "tenant",
            "project",
            "name",
            "topic_pattern",
            "device_id_mapping",
            "attribute_schema",
            "approval_required",
        ]
        read_only_fields = ["tenant", "project"]


class MqttSubscriptionHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = MqttSubscriptionHealth
        fields = ["agent", "connectivity", "received", "published", "backpressure", "updated_at"]


class IngestMessageSerializer(serializers.Serializer):
    topic = serializers.CharField()
    payload = serializers.JSONField()
    source_event_id = serializers.CharField(required=False, allow_blank=True, default="")


class StoragePolicySerializer(serializers.Serializer):
    storageDatapoint = serializers.BooleanField(required=False, default=True)
    mode = serializers.ChoiceField(
        choices=["all", "on_change", "min_interval", "fixed_n_per_window", "aggregate_window"], required=False
    )
    compare = serializers.DictField(required=False)
    max_samples = serializers.DictField(required=False)
    heartbeat = serializers.DictField(required=False)
