from django.urls import path
from rest_framework.routers import DefaultRouter

from spatial.views import ProjectMapConfigView, ScenePlacementViewSet, SceneViewSet

router = DefaultRouter()
router.register("scenes", SceneViewSet, basename="scene")
router.register("placements", ScenePlacementViewSet, basename="placement")

urlpatterns = router.urls + [
    path(
        "projects/<uuid:project_id>/map-config/",
        ProjectMapConfigView.as_view(),
        name="project-map-config",
    ),
]
