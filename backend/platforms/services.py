"""Platform services: audit and settings helpers."""

from __future__ import annotations

from core.authz import AuthzService
from core.errors import PermissionDeniedError


class AuditService:
    @staticmethod
    def record(*, actor, action, resource_type, resource_id="", tenant=None, project=None, payload=None):
        from platforms.models import AuditLog

        return AuditLog.objects.create(
            tenant=tenant,
            project=project,
            actor=actor,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            payload=payload or {},
        )


class ConfigService:
    """Resolve effective configuration: DB value prevails over env default.
    Environment variables seed the DB once (``seed-once``); afterwards the GUI
    edits the persisted value. Deployment locks always prevail.
    """

    @staticmethod
    def get_setting(key: str, default=None, *, tenant=None):
        from platforms.models import PlatformSetting

        qs = PlatformSetting.objects.filter(key=key)
        qs = qs.filter(tenant=tenant) if tenant is not None else qs.filter(tenant__isnull=True)
        setting = qs.first()
        if setting is not None:
            return setting.value
        return default

    @staticmethod
    def seed_once(key: str, value, *, tenant=None, is_mutable=True, source="env"):
        from platforms.models import PlatformSetting

        qs = PlatformSetting.objects.filter(key=key)
        qs = qs.filter(tenant=tenant) if tenant is not None else qs.filter(tenant__isnull=True)
        if qs.exists():
            return qs.first(), False
        obj = PlatformSetting.objects.create(tenant=tenant, key=key, value=value, source=source, is_mutable=is_mutable)
        return obj, True


def require_membership(user, tenant, permission: str):
    if not AuthzService.check(user, permission, tenant=tenant):
        raise PermissionDeniedError(f"Permission '{permission}' required.")


def purge_tenant_data(tenant) -> dict:
    """Delete all data owned by a tenant, in dependency order (no cascades)."""
    from assets.models import Asset, AssetAttribute
    from connectivity.models import Gateway, GatewayBinding
    from dashboards.models import Dashboard, Widget
    from platforms.models import AuditLog, Membership, PlatformSetting, Project
    from spatial.models import Scene, SceneLayer, ScenePlacement
    from telemetry.models import AttributeCurrent, IngestMetrics, StoragePolicyState, TelemetryPoint

    attribute_ids = list(AssetAttribute.objects.filter(tenant=tenant).values_list("id", flat=True))
    counts = {}
    counts["placements"] = ScenePlacement.objects.filter(asset__tenant=tenant).delete()[0]
    counts["bindings"] = GatewayBinding.objects.filter(tenant=tenant).delete()[0]
    counts["gateways"] = Gateway.objects.filter(tenant=tenant).delete()[0]
    counts["telemetry_points"] = TelemetryPoint.objects.filter(tenant_id=tenant.id).delete()[0]
    counts["currents"] = AttributeCurrent.objects.filter(tenant_id=tenant.id).delete()[0]
    counts["metrics"] = IngestMetrics.objects.filter(attribute_id__in=attribute_ids).delete()[0]
    counts["policy_states"] = StoragePolicyState.objects.filter(attribute_id__in=attribute_ids).delete()[0]
    counts["attributes"] = AssetAttribute.objects.filter(tenant=tenant).delete()[0]
    counts["assets"] = Asset.objects.filter(tenant=tenant).delete()[0]
    counts["widgets"] = Widget.objects.filter(dashboard__tenant=tenant).delete()[0]
    counts["dashboards"] = Dashboard.objects.filter(tenant=tenant).delete()[0]
    counts["scene_layers"] = SceneLayer.objects.filter(scene__tenant=tenant).delete()[0]
    counts["scenes"] = Scene.objects.filter(tenant=tenant).delete()[0]
    counts["audit"] = AuditLog.objects.filter(tenant=tenant).delete()[0]
    counts["settings"] = PlatformSetting.objects.filter(tenant=tenant).delete()[0]
    counts["memberships"] = Membership.objects.filter(tenant=tenant).delete()[0]
    counts["projects"] = Project.objects.filter(tenant=tenant).delete()[0]
    counts["tenant"] = tenant.delete()[0]
    return counts
