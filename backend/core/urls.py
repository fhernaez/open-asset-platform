from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import HealthView, LoginView, MeView

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me", MeView.as_view(), name="me"),
]
