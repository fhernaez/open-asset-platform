"""DRF permission classes enforcing tenant scoping and RBAC."""

from __future__ import annotations

from rest_framework import permissions

from core.authz import AuthzService


class IsTenantMember(permissions.BasePermission):
    message = "You are not a member of this tenant."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class TenantScopedPermission(permissions.BasePermission):
    """Require a domain permission; scoping to tenant/project is enforced in the
    queryset (see the TenantScopedViewSet) and on write in the serializer.
    """

    permission_required: str | None = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        required = getattr(view, "permission_required", None) or self.permission_required
        if required is None:
            return True
        return AuthzService.check(request.user, required)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        required = getattr(view, "permission_required", None) or self.permission_required
        if required is None:
            return True
        tenant = getattr(obj, "tenant", None)
        return AuthzService.check(request.user, required, tenant=tenant, project=getattr(obj, "project", None))
