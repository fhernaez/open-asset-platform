from django.urls import path
from rest_framework.routers import DefaultRouter

from telemetry.views import AttributeTelemetryViewSet, IngestView, TrendView

router = DefaultRouter()
router.register("attributes", AttributeTelemetryViewSet, basename="telemetry-attribute")

urlpatterns = router.urls + [
    path("ingest", IngestView.as_view(), name="telemetry-ingest"),
    path("trend", TrendView.as_view(), name="telemetry-trend"),
]
