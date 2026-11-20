from __future__ import annotations

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import TenantScopedPermission
from core.viewsets import TenantScopedViewSet
from dashboards.models import Dashboard, DashboardBundle, DashboardTemplate, Widget
from dashboards.serializers import (
    DashboardBundleSerializer,
    DashboardSerializer,
    DashboardTemplateSerializer,
    WidgetSerializer,
)
from platforms.services import require_membership

SCADA_SYMBOLS = [
    {"key": "pump", "label_i18n": {"es": "Bomba", "en": "Pump"}, "categories": ["hvac", "water"]},
    {"key": "fan", "label_i18n": {"es": "Ventilador", "en": "Fan"}, "categories": ["hvac"]},
    {"key": "chiller", "label_i18n": {"es": "Enfriadora", "en": "Chiller"}, "categories": ["hvac"]},
    {"key": "boiler", "label_i18n": {"es": "Caldera", "en": "Boiler"}, "categories": ["hvac"]},
    {"key": "valve", "label_i18n": {"es": "Válvula", "en": "Valve"}, "categories": ["water", "generic"]},
    {"key": "motor", "label_i18n": {"es": "Motor", "en": "Motor"}, "categories": ["generic"]},
    {"key": "tank", "label_i18n": {"es": "Tanque", "en": "Tank"}, "categories": ["water"]},
    {"key": "sensor", "label_i18n": {"es": "Sensor", "en": "Sensor"}, "categories": ["generic"]},
    {"key": "meter", "label_i18n": {"es": "Medidor", "en": "Meter"}, "categories": ["energy"]},
    {"key": "generator", "label_i18n": {"es": "Generador", "en": "Generator"}, "categories": ["energy"]},
]


def _definition(dashboard: Dashboard) -> dict:
    return {
        "dashboard": {
            "name": dashboard.name,
            "description": dashboard.description,
            "grid_cols": dashboard.grid_cols,
            "grid_rows": dashboard.grid_rows,
        },
        "widgets": [
            {
                "title": w.title,
                "widget_type": w.widget_type,
                "x": w.x,
                "y": w.y,
                "w": w.w,
                "h": w.h,
                "config": w.config,
            }
            for w in dashboard.widgets.all()
        ],
    }


def _apply_definition(tenant, project, definition: dict) -> Dashboard:
    meta = definition.get("dashboard") or {}
    dashboard = Dashboard.objects.create(
        tenant=tenant,
        project=project,
        name=str(meta.get("name") or "Imported dashboard")[:200],
        description=str(meta.get("description") or "")[:500],
        grid_cols=int(meta.get("grid_cols") or 12),
        grid_rows=int(meta.get("grid_rows") or 6),
    )
    for w in definition.get("widgets") or []:
        if not isinstance(w, dict):
            continue
        Widget.objects.create(
            dashboard=dashboard,
            title=str(w.get("title") or "")[:160],
            widget_type=w.get("widget_type") or "line",
            x=int(w.get("x") or 0),
            y=int(w.get("y") or 0),
            w=int(w.get("w") or 4),
            h=int(w.get("h") or 3),
            config=w.get("config") or {},
        )
    return dashboard


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

    @action(detail=True, methods=["post"], url_path="export-bundle")
    def export_bundle(self, request, pk=None):
        """Export the dashboard + widgets as a DashboardBundle (ADR-019)."""
        dashboard = self.get_object()
        name = request.data.get("name") or f"{dashboard.name} (bundle)"
        bundle = DashboardBundle.objects.create(
            tenant=dashboard.tenant,
            project=dashboard.project,
            name=str(name)[:200],
            description=str(request.data.get("description") or "")[:500],
            data=_definition(dashboard),
        )
        return Response(DashboardBundleSerializer(bundle).data, status=status.HTTP_201_CREATED)


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


class DashboardBundleViewSet(TenantScopedViewSet):
    serializer_class = DashboardBundleSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.view"
    tenant_field = "tenant_id"
    queryset = DashboardBundle.objects.all()

    @action(detail=True, methods=["post"], url_path="import")
    def import_dashboard(self, request, pk=None):
        """Create a new dashboard from the bundle data (same tenant)."""
        bundle = self.get_object()
        tenant = bundle.tenant
        require_membership(request.user, tenant, "assets.manage")
        dashboard = _apply_definition(tenant, bundle.project, bundle.data)
        return Response(DashboardSerializer(dashboard).data, status=status.HTTP_201_CREATED)


class DashboardTemplateViewSet(TenantScopedViewSet):
    serializer_class = DashboardTemplateSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.view"
    tenant_field = "tenant_id"
    queryset = DashboardTemplate.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs

    @action(detail=True, methods=["post"], url_path="apply")
    def apply_template(self, request, pk=None):
        """Instantiate the template as a new dashboard (same tenant)."""
        template = self.get_object()
        require_membership(request.user, template.tenant, "assets.manage")
        name = request.data.get("name") or template.name
        definition = dict(template.definition or {})
        definition.setdefault("dashboard", {})["name"] = name
        dashboard = _apply_definition(template.tenant, template.project, definition)
        return Response(DashboardSerializer(dashboard).data, status=status.HTTP_201_CREATED)


class SymbolsCatalogView(APIView):
    """SCADA symbol catalog for map/SCADA widgets (ADR-019, P2 basic catalog)."""

    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.view"

    @extend_schema(responses={"200": OpenApiTypes.OBJECT})
    def get(self, request):
        return Response({"symbols": SCADA_SYMBOLS})
