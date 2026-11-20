from django.urls import path
from rest_framework.routers import DefaultRouter

from dashboards.views import (
    DashboardBundleViewSet,
    DashboardTemplateViewSet,
    DashboardViewSet,
    SymbolsCatalogView,
    WidgetViewSet,
)

router = DefaultRouter()
router.register("", DashboardViewSet, basename="dashboard")
router.register("bundles", DashboardBundleViewSet, basename="dashboard-bundle")
router.register("templates", DashboardTemplateViewSet, basename="dashboard-template")

urlpatterns = [
    path("symbols/", SymbolsCatalogView.as_view(), name="dashboard-symbols"),
    path("widgets/", WidgetViewSet.as_view({"get": "list", "post": "create"}), name="widget-list"),
    path(
        "widgets/<uuid:pk>/",
        WidgetViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="widget-detail",
    ),
] + router.urls
