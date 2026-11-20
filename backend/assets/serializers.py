from __future__ import annotations

from rest_framework import serializers

from assets.models import Asset, AssetAttribute, AssetType, Unit


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["symbol", "name", "quantity"]


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = [
            "id",
            "tenant",
            "project",
            "name",
            "code",
            "kind",
            "is_location",
            "description",
            "schema",
            "created_at",
        ]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }

    def validate_schema(self, value):
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise serializers.ValidationError("schema must be an object.")
        attributes = value.get("attributes")
        if attributes is not None:
            if not isinstance(attributes, list):
                raise serializers.ValidationError("schema.attributes must be a list.")
            for item in attributes:
                if not isinstance(item, dict) or not item.get("code") or not item.get("value_type"):
                    raise serializers.ValidationError("each schema.attributes item needs code and value_type.")
        return value


class AssetSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            "id",
            "tenant",
            "project",
            "name",
            "external_ref",
            "asset_type",
            "parent",
            "status",
            "metadata",
            "latitude",
            "longitude",
            "rel_x",
            "rel_y",
            "geofence",
            "image",
            "image_url",
            "designations",
            "created_at",
        ]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image:
            return None
        url = obj.image.url
        if request:
            return request.build_absolute_uri(url)
        return url


class AssetAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetAttribute
        fields = [
            "id",
            "tenant",
            "project",
            "asset",
            "name",
            "code",
            "value_type",
            "unit",
            "description",
            "storage_datapoint",
            "history_enabled",
            "history_policy_override",
            "metadata",
            "auto_discovered",
            "is_active",
            "created_at",
        ]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }

    def validate(self, attrs):
        override = attrs.get("history_policy_override")
        if override is not None and not isinstance(override, dict):
            raise serializers.ValidationError({"history_policy_override": "must be an object"})
        mode = (override or {}).get("mode")
        if mode is not None and mode not in {
            "all",
            "on_change",
            "min_interval",
            "fixed_n_per_window",
            "aggregate_window",
        }:
            raise serializers.ValidationError({"history_policy_override": "invalid mode"})
        # storageDatapoint is the UI alias of history_enabled (internal source of truth).
        if "history_enabled" in attrs and "storage_datapoint" not in attrs:
            attrs["storage_datapoint"] = attrs["history_enabled"]
        if "storage_datapoint" in attrs and "history_enabled" not in attrs:
            attrs["history_enabled"] = attrs["storage_datapoint"]
        return attrs
