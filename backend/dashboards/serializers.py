from __future__ import annotations

from rest_framework import serializers

from dashboards.models import Dashboard, Widget


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ["id", "dashboard", "title", "widget_type", "x", "y", "w", "h", "config"]
        extra_kwargs = {"dashboard": {"required": False}}


class DashboardSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = ["id", "tenant", "project", "name", "description", "grid_cols", "grid_rows", "widgets"]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }
