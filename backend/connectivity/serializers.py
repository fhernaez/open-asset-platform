from __future__ import annotations

from rest_framework import serializers

from connectivity.models import Gateway, GatewayBinding


class GatewaySerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    asset_code = serializers.CharField(source="asset.asset_type.code", read_only=True)

    class Meta:
        model = Gateway
        fields = [
            "id",
            "tenant",
            "project",
            "asset",
            "asset_name",
            "asset_code",
            "protocol",
            "config",
            "connection_status",
        ]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }
        read_only_fields = ["connection_status"]


class GatewayBindingSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    attribute_code = serializers.CharField(source="attribute.code", read_only=True, allow_null=True)
    address = serializers.CharField(validators=[])

    class Meta:
        model = GatewayBinding
        fields = [
            "id",
            "tenant",
            "project",
            "gateway",
            "binding_type",
            "asset",
            "asset_name",
            "attribute",
            "attribute_code",
            "address",
            "mapping",
            "qos",
            "polling",
        ]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = dict(data)
            if isinstance(data.get("address"), str):
                data["address"] = "".join(ch for ch in data["address"] if ord(ch) >= 32).strip()
        return super().to_internal_value(data)

    def validate(self, attrs):
        binding_type = attrs.get("binding_type", "attribute")
        if binding_type == "attribute" and not attrs.get("attribute"):
            raise serializers.ValidationError({"attribute": "required for attribute bindings."})
        if binding_type == "device" and attrs.get("attribute"):
            attrs["attribute"] = None
        return attrs

    def validate_address(self, value):
        cleaned = "".join(ch for ch in value if ord(ch) >= 32).strip()
        return cleaned
