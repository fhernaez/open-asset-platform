"""Spatial bounded context: scenes (image layers) and asset placements (ADR-015)."""

from __future__ import annotations

from django.db import models

from platforms.models import TenantScopedModel


def scene_image_path(instance, filename: str) -> str:
    scene = instance.scene
    return f"scenes/{scene.tenant_id}/{scene.id}/{filename}"


class ProjectMapConfig(TenantScopedModel):
    """Geo map configuration for a project (ADR-015 v2).

    Bounds define the rectangle where assets are located; the user draws it by
    navigating the global map (MapLibre + OpenStreetMap, free).
    """

    provider = models.CharField(max_length=32, default="maplibre")
    north = models.FloatField(null=True, blank=True)
    south = models.FloatField(null=True, blank=True)
    east = models.FloatField(null=True, blank=True)
    west = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "spatial_projectmapconfig"
        unique_together = [("tenant", "project")]

    def __str__(self) -> str:
        return f"map-config:{self.project_id}"


class Scene(TenantScopedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")

    class Meta:
        db_table = "spatial_scene"

    def __str__(self) -> str:
        return self.name


class SceneLayer(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="layers")
    key = models.CharField(max_length=80)
    name = models.CharField(max_length=160, blank=True, default="")
    image = models.ImageField(upload_to=scene_image_path, max_length=255)
    opacity = models.FloatField(default=1.0)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = "spatial_scenelayer"
        unique_together = [("scene", "key")]
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.scene.name}/{self.key}"


class ScenePlacement(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="placements")
    layer = models.ForeignKey(SceneLayer, on_delete=models.CASCADE, null=True, blank=True, related_name="placements")
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE, related_name="scene_placements")
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    z = models.IntegerField(default=0)

    class Meta:
        db_table = "spatial_sceneplacement"
        unique_together = [("scene", "asset")]

    def __str__(self) -> str:
        return f"{self.scene.name}/{self.asset.name}"
