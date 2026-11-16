"""Asset services exposed to plugins (public contract)."""

from __future__ import annotations

from core.authz import AuthzService
from core.errors import NotFoundError, PermissionDeniedError


class AssetService:
    @staticmethod
    def get(asset_id, ctx):
        from assets.models import Asset

        try:
            asset = Asset.objects.select_related("tenant", "project", "asset_type").get(id=asset_id)
        except Asset.DoesNotExist:
            raise NotFoundError("Asset not found.") from None
        if not AuthzService.check(ctx.actor, "assets.view", tenant=asset.tenant, project=asset.project):
            raise PermissionDeniedError("assets.view required.")
        return asset

    @staticmethod
    def list(ctx, *, tenant_id=None, project_id=None):
        from assets.models import Asset

        qs = Asset.objects.all()
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs


class AttributeService:
    @staticmethod
    def get(attribute_id, ctx):
        from assets.models import AssetAttribute

        try:
            attr = AssetAttribute.objects.select_related("asset", "tenant", "project").get(id=attribute_id)
        except AssetAttribute.DoesNotExist:
            raise NotFoundError("Attribute not found.") from None
        if not AuthzService.check(ctx.actor, "assets.view", tenant=attr.tenant, project=attr.project):
            raise PermissionDeniedError("assets.view required.")
        return attr
