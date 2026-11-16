"""Plugin manager bounded context: definitions, installations, activation, settings."""

from __future__ import annotations

from django.db import models

from core.models import UUIDPkModel


class PluginDefinition(UUIDPkModel):
    class Kind(models.TextChoices):
        DJANGO_APP = "django_app"
        SERVICE = "service"

    slug = models.SlugField(max_length=120, unique=True)
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=32)
    core_contract = models.CharField(max_length=64, blank=True, default="")
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.DJANGO_APP)
    requires = models.JSONField(default=list, blank=True)
    provides = models.JSONField(default=list, blank=True)
    permissions = models.JSONField(default=list, blank=True)
    is_core = models.BooleanField(default=False)
    health_status = models.CharField(
        max_length=16,
        choices=[
            ("unknown", "unknown"),
            ("healthy", "healthy"),
            ("unhealthy", "unhealthy"),
            ("incompatible", "incompatible"),
        ],
        default="unknown",
    )

    class Meta:
        db_table = "plugins_plugindefinition"
        ordering = ["slug"]

    def __str__(self) -> str:
        return self.slug


class PluginInstallation(UUIDPkModel):
    definition = models.ForeignKey(PluginDefinition, on_delete=models.CASCADE, related_name="installations")
    version = models.CharField(max_length=32)
    installed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plugins_plugininstallation"
        unique_together = [("definition", "version")]


class PluginActivation(UUIDPkModel):
    definition = models.ForeignKey(PluginDefinition, on_delete=models.CASCADE, related_name="activations")
    tenant = models.ForeignKey("platforms.Tenant", on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    project = models.ForeignKey("platforms.Project", on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    enabled = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    class Meta:
        db_table = "plugins_pluginactivation"
        unique_together = [("definition", "tenant", "project")]


class PluginSettings(UUIDPkModel):
    definition = models.ForeignKey(PluginDefinition, on_delete=models.CASCADE, related_name="settings")
    tenant = models.ForeignKey("platforms.Tenant", on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    value = models.JSONField(default=dict, blank=True)
    is_mutable = models.BooleanField(default=True)
    updated_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    class Meta:
        db_table = "plugins_pluginsettings"
        unique_together = [("definition", "tenant")]
