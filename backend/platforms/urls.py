from rest_framework.routers import DefaultRouter

from platforms.views import (
    AuditLogViewSet,
    MembershipViewSet,
    PlatformSettingViewSet,
    ProjectViewSet,
    TenantViewSet,
)

router = DefaultRouter()
router.register("tenants", TenantViewSet, basename="tenant")
router.register("projects", ProjectViewSet, basename="project")
router.register("memberships", MembershipViewSet, basename="membership")
router.register("audit", AuditLogViewSet, basename="audit")
router.register("settings", PlatformSettingViewSet, basename="platform-setting")

urlpatterns = router.urls
