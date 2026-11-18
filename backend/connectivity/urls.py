from rest_framework.routers import DefaultRouter

from connectivity.views import GatewayBindingViewSet, GatewayViewSet

router = DefaultRouter()
router.register("gateways", GatewayViewSet, basename="connectivity-gateway")
router.register("bindings", GatewayBindingViewSet, basename="connectivity-binding")

urlpatterns = router.urls
