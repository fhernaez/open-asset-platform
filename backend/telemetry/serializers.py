from __future__ import annotations

from rest_framework import serializers


class IngestEventSerializer(serializers.Serializer):
    tenant_id = serializers.UUIDField()
    project_id = serializers.UUIDField(required=False, allow_null=True)
    asset_id = serializers.UUIDField()
    attribute_id = serializers.UUIDField()
    observed_at = serializers.DateTimeField()
    value = serializers.JSONField()
    value_type = serializers.ChoiceField(choices=["string", "boolean", "number", "json"])
    quality = serializers.CharField(default="good")
    source_event_id = serializers.CharField(required=False, allow_blank=True, default="")
    sequence = serializers.IntegerField(required=False, allow_null=True)
    transport = serializers.CharField(required=False, default="mqtt")
    topic = serializers.CharField(required=False, allow_blank=True, default="")
