from __future__ import annotations

from django.conf import settings
from django.db import connection
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.serializers import TokenObtainPairSerializer, UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    pass


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=UserSerializer)
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class HealthView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        responses=inline_serializer(
            name="Health",
            fields={
                "status": serializers.CharField(),
                "service": serializers.CharField(),
                "version": serializers.CharField(),
                "database": serializers.CharField(),
            },
        )
    )
    def get(self, request):
        db_ok = True
        try:
            connection.ensure_connection()
        except Exception:  # pragma: no cover - exercised only when DB down
            db_ok = False
        return Response(
            {
                "status": "ok" if db_ok else "degraded",
                "service": "oap-api",
                "version": getattr(settings, "OAP_VERSION", "0.1.0"),
                "database": "up" if db_ok else "down",
            },
            status=200 if db_ok else 503,
        )
