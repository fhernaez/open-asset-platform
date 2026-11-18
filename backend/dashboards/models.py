"""Dashboards bounded context: dashboard grid + widgets (ADR-015)."""

from __future__ import annotations

from django.db import models

from platforms.models import TenantScopedModel


class Dashboard(TenantScopedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    grid_cols = models.IntegerField(default=12)
    grid_rows = models.IntegerField(default=6)

    class Meta:
        db_table = "dashboards_dashboard"

    def __str__(self) -> str:
        return self.name


class Widget(models.Model):
    class WidgetType(models.TextChoices):
        LINE = "line"
        GAUGE = "gauge"
        CARD = "card"
        TABLE = "table"
        MAP = "map"

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name="widgets")
    title = models.CharField(max_length=160, blank=True, default="")
    widget_type = models.CharField(max_length=16, choices=WidgetType.choices, default=WidgetType.LINE)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    w = models.IntegerField(default=4)
    h = models.IntegerField(default=3)
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "dashboards_widget"
        ordering = ["y", "x"]

    def __str__(self) -> str:
        return f"{self.dashboard.name}/{self.title or self.widget_type}"
