"""Base viewset enforcing tenant scoping and request context."""

from __future__ import annotations

from dataclasses import dataclass, field

from rest_framework import viewsets

from core.errors import PermissionDeniedError


@dataclass
class RequestContext:
    actor_id: str
    tenant_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    extra: dict = field(default_factory=dict)


def request_context(request) -> RequestContext:
    tenant = getattr(request, "tenant", None)
    project = getattr(request, "project", None)
    return RequestContext(
        actor_id=str(request.user.id),
        tenant_id=str(tenant.id) if tenant is not None else None,
        project_id=str(project.id) if project is not None else None,
        trace_id=request.META.get("HTTP_X_REQUEST_ID"),
    )


class TenantScopedViewSet(viewsets.ModelViewSet):
    """ModelViewSet that scopes the queryset to the tenant/project of the caller.

    ``tenant_lookup`` names the attribute used to derive the tenant from the
    request (e.g. a header or a project header). By default the tenant is read
    from ``request.tenant`` which is populated by middleware or by the model
    instance itself for object-level checks.
    """

    permission_classes = []
    permission_required: str | None = None

    def get_queryset(self):
        qs = super().get_queryset()
        return self._scope_queryset(qs)

    def _scope_queryset(self, qs):
        if getattr(self, "unscoped", False):
            return qs
        user = self.request.user
        if user.is_superuser or getattr(user, "is_platform_admin", False):
            return qs
        from platforms.models import Membership

        tenant_ids = list(Membership.objects.filter(user=user, is_active=True).values_list("tenant_id", flat=True))
        if not tenant_ids:
            return qs.none()
        field = getattr(self, "tenant_field", "tenant_id")
        return qs.filter(**{f"{field}__in": tenant_ids})


def require_perm(request, permission: str, *, tenant=None, project=None):
    from core.authz import AuthzService

    if not AuthzService.check(request.user, permission, tenant=tenant, project=project):
        raise PermissionDeniedError(f"Permission '{permission}' required.")
