from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("core.urls")),
    path("api/v1/platform/", include("platforms.urls")),
    path("api/v1/assets/", include("assets.urls")),
    path("api/v1/telemetry/", include("telemetry.urls")),
    path("api/v1/plugins/", include("plugins.urls")),
    path("api/v1/mqtt/", include("mqtt.urls")),
]
