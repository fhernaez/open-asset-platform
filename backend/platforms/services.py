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
