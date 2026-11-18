from __future__ import annotations

from rest_framework import parsers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import TenantScopedPermission
from core.viewsets import TenantScopedViewSet
from platforms.services import require_membership
from spatial.models import Scene, SceneLayer, ScenePlacement
from spatial.serializers import SceneLayerSerializer, ScenePlacementSerializer, SceneSerializer


class SceneViewSet(TenantScopedViewSet):
    serializer_class = SceneSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.view"
    tenant_field = "tenant_id"
    queryset = Scene.objects.prefetch_related("layers", "placements__asset").all()

    def perform_create(self, serializer):
        tenant = serializer.validated_data.get("tenant")
        if tenant is None:
            from platforms.models import Membership

            membership = Membership.objects.filter(user=self.request.user, is_active=True).first()
            tenant = membership.tenant if membership else None
        require_membership(self.request.user, tenant, "assets.view")
        serializer.save(tenant=tenant)

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        serializer.save()

    @action(
        detail=True, methods=["post"], parser_classes=[parsers.MultiPartParser, parsers.FormParser], url_path="layers"
    )
    def add_layer(self, request, pk=None):
        scene = self.get_object()
        key = request.data.get("key", "").strip()
        if not key:
            return Response({"detail": "key is required."}, status=400)
        layer, _ = SceneLayer.objects.update_or_create(
            scene=scene,
            key=key,
            defaults={
                "name": request.data.get("name", key),
                "image": request.FILES.get("image"),
                "opacity": float(request.data.get("opacity", 1.0)),
                "order": int(request.data.get("order", 0)),
            },
        )
        return Response(SceneLayerSerializer(layer, context={"request": request}).data, status=status.HTTP_201_CREATED)


class ScenePlacementViewSet(TenantScopedViewSet):
    serializer_class = ScenePlacementSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.view"
    tenant_field = "scene__tenant_id"
    queryset = ScenePlacement.objects.select_related("scene", "asset").all()

    def get_queryset(self):
        qs = super().get_queryset()
        scene_id = self.request.query_params.get("scene")
        if scene_id:
            qs = qs.filter(scene_id=scene_id)
        return qs
