from rest_framework.routers import DefaultRouter

from spatial.views import ScenePlacementViewSet, SceneViewSet

router = DefaultRouter()
router.register("scenes", SceneViewSet, basename="scene")
router.register("placements", ScenePlacementViewSet, basename="placement")

urlpatterns = router.urls
