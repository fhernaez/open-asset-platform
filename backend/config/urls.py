from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/schema/swagger", SpectacularSwaggerView.as_view(url_name="schema"), name="schema-swagger"),
    path("api/v1/", include("core.urls")),
    path("api/v1/platform/", include("platforms.urls")),
    path("api/v1/assets/", include("assets.urls")),
    path("api/v1/telemetry/", include("telemetry.urls")),
    path("api/v1/plugins/", include("plugins.urls")),
    path("api/v1/connectivity/", include("connectivity.urls")),
    path("api/v1/dashboards/", include("dashboards.urls")),
    path("api/v1/spatial/", include("spatial.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
