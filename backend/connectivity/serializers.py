from __future__ import annotations

from rest_framework import serializers

from connectivity.models import Gateway, GatewayBinding


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ["id", "tenant", "project", "asset", "protocol", "config", "connection_status"]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }
        read_only_fields = ["connection_status"]


class GatewayBindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayBinding
        fields = ["id", "tenant", "project", "gateway", "asset", "attribute", "address", "mapping", "qos", "polling"]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }
