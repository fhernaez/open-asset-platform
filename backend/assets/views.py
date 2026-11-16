from __future__ import annotations

from rest_framework.permissions import IsAuthenticated

from assets.models import Asset, AssetAttribute, AssetType, Unit
from assets.serializers import (
    AssetAttributeSerializer,
    AssetSerializer,
    AssetTypeSerializer,
    UnitSerializer,
)
from core.permissions import TenantScopedPermission
from core.viewsets import TenantScopedViewSet
from platforms.services import AuditService, require_membership


class UnitViewSet(TenantScopedViewSet):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    queryset = Unit.objects.all()
    unscoped = True


class AssetTypeViewSet(TenantScopedViewSet):
    serializer_class = AssetTypeSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.manage"
    tenant_field = "tenant_id"
    queryset = AssetType.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save(tenant=self._tenant_for_request())
        AuditService.record(
            actor=self.request.user,
            action="assettype.create",
            resource_type="assettype",
            resource_id=str(obj.id),
            tenant=obj.tenant,
        )

    def _tenant_for_request(self):
        from platforms.models import Membership

        tenant_id = self.request.data.get("tenant") or self.request.query_params.get("tenant")
        if tenant_id:
            from platforms.models import Tenant

            return Tenant.objects.get(id=tenant_id)
        membership = Membership.objects.filter(user=self.request.user, is_active=True).first()
        return membership.tenant if membership else None


class AssetViewSet(TenantScopedViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.manage"
    tenant_field = "tenant_id"
    queryset = Asset.objects.select_related("asset_type", "parent").all()

    def get_permissions(self):
        perms = super().get_permissions()
        return perms

    def perform_create(self, serializer):
        tenant = self._resolve_tenant(serializer.validated_data)
        require_membership(self.request.user, tenant, "assets.manage")
        asset = serializer.save(tenant=tenant)
        AuditService.record(
            actor=self.request.user,
            action="asset.create",
            resource_type="asset",
            resource_id=str(asset.id),
            tenant=tenant,
        )

    def perform_update(self, serializer):
        asset = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="asset.update",
            resource_type="asset",
            resource_id=str(asset.id),
            tenant=asset.tenant,
        )

    def _resolve_tenant(self, data):
        from platforms.models import Membership, Tenant

        tenant_id = data.get("tenant") or getattr(self.request, "tenant_id", None)
        if tenant_id:
            return Tenant.objects.get(id=tenant_id)
        membership = Membership.objects.filter(user=self.request.user, is_active=True).first()
        if not membership:
            from core.errors import PermissionDeniedError

            raise PermissionDeniedError("No active tenant membership.")
        return membership.tenant


class AssetAttributeViewSet(TenantScopedViewSet):
    serializer_class = AssetAttributeSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.manage"
    tenant_field = "tenant_id"
    queryset = AssetAttribute.objects.select_related("asset", "unit").all()

    def perform_create(self, serializer):
        attr = serializer.save(tenant=self._tenant_for_asset(serializer.validated_data))
        AuditService.record(
            actor=self.request.user,
            action="attribute.create",
            resource_type="attribute",
            resource_id=str(attr.id),
            tenant=attr.tenant,
        )

    def _tenant_for_asset(self, data):
        asset = data.get("asset")
        return asset.tenant
