from django.urls import path
from rest_framework.routers import DefaultRouter

from telemetry.views import AttributeTelemetryViewSet, IngestView

router = DefaultRouter()
router.register("attributes", AttributeTelemetryViewSet, basename="telemetry-attribute")

urlpatterns = router.urls + [
    path("ingest", IngestView.as_view(), name="telemetry-ingest"),
]
