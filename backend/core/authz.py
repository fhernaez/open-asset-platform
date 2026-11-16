"""Authorization service: RBAC scoped to tenant/project, deny-by-default."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from core.models import User


class AuthzService:
    """Resolve whether a principal may perform an action.

    Wildcard permissions ``*`` (platform admin) and ``<domain>.*`` are
    supported. By default access is denied.
    """

    @staticmethod
    def has_permission(principal: User, permission: str) -> bool:
        if not principal or not principal.is_authenticated:
            return False
        if principal.is_superuser or getattr(principal, "is_platform_admin", False):
            return True
        return False

    @staticmethod
    def check(
        principal: User,
        permission: str,
        *,
        tenant=None,
        project=None,
    ) -> bool:
        if not principal or not principal.is_authenticated:
            return False
        if principal.is_superuser or getattr(principal, "is_platform_admin", False):
            return True

        from platforms.models import Membership

        memberships = Membership.objects.filter(
            user=principal,
            tenant_id=tenant.id if tenant is not None else None,
            is_active=True,
        )
        if tenant is None:
            memberships = Membership.objects.filter(user=principal, is_active=True)

        domain = permission.split(".")[0]
        for membership in memberships.select_related("role"):
            perms = membership.role.permissions or []
            if "*" in perms or permission in perms or f"{domain}.*" in perms:
                return True
        return False
