from __future__ import annotations

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import TenantScopedPermission
from plugins.models import PluginDefinition, PluginSettings
from plugins.serializers import PluginSerializer, PluginSettingsSerializer
from plugins.services import PluginManager


class PluginViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PluginSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "plugins.view"
    queryset = PluginDefinition.objects.all()
    lookup_field = "slug"
    lookup_value_regex = r"[^/]+"

    def list(self, request, *args, **kwargs):
        return Response(PluginManager.list_plugins())

    @action(
        detail=True,
        methods=["patch"],
        url_path="activation",
        permission_classes=[IsAuthenticated, TenantScopedPermission],
    )
    def activation(self, request, slug=None):
        self.permission_required = "plugins.configure"
        self.check_permissions(request)
        enabled = request.data.get("enabled")
        if enabled is None:
            from core.errors import ValidationError

            raise ValidationError("'enabled' is required.")
        result = PluginManager.set_enabled(slug, bool(enabled), actor=request.user)
        return Response(result)

    @action(detail=True, methods=["get"], url_path="health")
    def health(self, request, slug=None):
        definition = self.get_object()
        return Response({"slug": slug, "health": definition.health_status})


class PluginSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = PluginSettingsSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "plugins.configure"
    queryset = PluginSettings.objects.all()
