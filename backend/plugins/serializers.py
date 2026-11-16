from __future__ import annotations

from rest_framework import serializers

from plugins.models import PluginActivation, PluginDefinition, PluginSettings


class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginDefinition
        fields = ["slug", "name", "version", "kind", "is_core", "requires", "provides", "permissions", "health_status"]


class PluginActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginActivation
        fields = ["definition", "tenant", "project", "enabled", "locked"]
        read_only_fields = ["definition", "tenant", "project", "locked"]


class PluginSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginSettings
        fields = ["definition", "tenant", "value", "is_mutable", "updated_at"]
        read_only_fields = ["definition", "tenant", "updated_at"]
