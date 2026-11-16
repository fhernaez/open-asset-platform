from rest_framework.routers import DefaultRouter

from plugins.views import PluginSettingsViewSet, PluginViewSet

router = DefaultRouter()
router.register("", PluginViewSet, basename="plugin")
router.register("settings", PluginSettingsViewSet, basename="plugin-settings")

urlpatterns = router.urls
