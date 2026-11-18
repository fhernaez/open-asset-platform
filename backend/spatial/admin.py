from django.contrib import admin

from spatial.models import Scene, SceneLayer, ScenePlacement


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ["name", "tenant", "project"]


@admin.register(SceneLayer)
class SceneLayerAdmin(admin.ModelAdmin):
    list_display = ["scene", "key", "order"]


@admin.register(ScenePlacement)
class ScenePlacementAdmin(admin.ModelAdmin):
    list_display = ["scene", "asset", "x", "y", "z"]
