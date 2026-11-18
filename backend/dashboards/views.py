from __future__ import annotations

from rest_framework.permissions import IsAuthenticated

from core.permissions import TenantScopedPermission
from core.viewsets import TenantScopedViewSet
from dashboards.models import Dashboard, Widget
from dashboards.serializers import DashboardSerializer, WidgetSerializer
from platforms.services import require_membership


class DashboardViewSet(TenantScopedViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.view"
    tenant_field = "tenant_id"
    lookup_value_regex = "[0-9a-fA-F-]{36}"
    queryset = Dashboard.objects.prefetch_related("widgets").all()

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


class WidgetViewSet(TenantScopedViewSet):
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.view"
    tenant_field = "dashboard__tenant_id"
    queryset = Widget.objects.select_related("dashboard").all()

    def get_queryset(self):
        qs = super().get_queryset()
        dashboard_id = self.request.query_params.get("dashboard")
        if dashboard_id:
            qs = qs.filter(dashboard_id=dashboard_id)
        return qs
