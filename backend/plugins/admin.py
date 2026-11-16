from __future__ import annotations

from django.contrib import admin

from plugins.models import PluginActivation, PluginDefinition, PluginInstallation, PluginSettings


@admin.register(PluginDefinition)
class PluginDefinitionAdmin(admin.ModelAdmin):
    list_display = ["slug", "name", "version", "kind", "is_core", "health_status"]


@admin.register(PluginInstallation)
class PluginInstallationAdmin(admin.ModelAdmin):
    list_display = ["definition", "version", "installed_at"]


@admin.register(PluginActivation)
class PluginActivationAdmin(admin.ModelAdmin):
    list_display = ["definition", "tenant", "enabled", "locked"]


@admin.register(PluginSettings)
class PluginSettingsAdmin(admin.ModelAdmin):
    list_display = ["definition", "tenant", "is_mutable"]
