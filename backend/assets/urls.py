from rest_framework.routers import DefaultRouter

from assets.views import AssetAttributeViewSet, AssetTypeViewSet, AssetViewSet, UnitViewSet

router = DefaultRouter()
router.register("units", UnitViewSet, basename="unit")
router.register("types", AssetTypeViewSet, basename="asset-type")
router.register("assets", AssetViewSet, basename="asset")
router.register("attributes", AssetAttributeViewSet, basename="attribute")

urlpatterns = router.urls
