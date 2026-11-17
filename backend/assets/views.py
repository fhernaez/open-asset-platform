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

    def get_queryset(self):
        qs = super().get_queryset()
        tenant_id = self.request.query_params.get("tenant")
        kind = self.request.query_params.get("kind")
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        if kind:
            qs = qs.filter(kind=kind)
        return qs

    def perform_create(self, serializer):
        obj = serializer.save(tenant=self._tenant_for_request())
        AuditService.record(
            actor=self.request.user,
            action="assettype.create",
            resource_type="assettype",
            resource_id=str(obj.id),
            tenant=obj.tenant,
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        obj = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="assettype.update",
            resource_type="assettype",
            resource_id=str(obj.id),
            tenant=obj.tenant,
        )

    def _tenant_for_request(self):
        from platforms.models import Membership, Tenant

        tenant = self.request.data.get("tenant")
        if tenant:
            return Tenant.objects.get(id=tenant)
        membership = Membership.objects.filter(user=self.request.user, is_active=True).first()
        return membership.tenant if membership else None


class AssetViewSet(TenantScopedViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.manage"
    tenant_field = "tenant_id"
    queryset = Asset.objects.select_related("asset_type", "parent").all()

    def get_queryset(self):
        qs = super().get_queryset()
        tenant_id = self.request.query_params.get("tenant")
        project_id = self.request.query_params.get("project")
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs

    def perform_create(self, serializer):
        tenant = self._resolve_tenant(serializer.validated_data)
        require_membership(self.request.user, tenant, "assets.manage")
        project = serializer.validated_data.get("project")
        if project is not None and project.tenant_id != tenant.id:
            from core.errors import ValidationError

            raise ValidationError("project must belong to the asset tenant.")
        asset = serializer.save(tenant=tenant)
        from assets.services import apply_type_template

        apply_type_template(asset)
        AuditService.record(
            actor=self.request.user,
            action="asset.create",
            resource_type="asset",
            resource_id=str(asset.id),
            tenant=tenant,
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        asset = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="asset.update",
            resource_type="asset",
            resource_id=str(asset.id),
            tenant=asset.tenant,
        )

    def _resolve_tenant(self, data):
        from platforms.models import Membership

        tenant = data.get("tenant")
        if tenant is not None:
            return tenant
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

    def get_queryset(self):
        qs = super().get_queryset()
        asset_id = self.request.query_params.get("asset")
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        return qs

    def perform_create(self, serializer):
        asset = serializer.validated_data.get("asset")
        if asset is None:
            from core.errors import ValidationError

            raise ValidationError("asset is required.")
        require_membership(self.request.user, asset.tenant, "assets.manage")
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        attr = serializer.save(tenant=asset.tenant, project=asset.project)
        AuditService.record(
            actor=self.request.user,
            action="attribute.create",
            resource_type="attribute",
            resource_id=str(attr.id),
            tenant=attr.tenant,
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        attr = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="attribute.update",
            resource_type="attribute",
            resource_id=str(attr.id),
            tenant=attr.tenant,
        )
