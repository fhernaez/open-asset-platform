from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import TenantScopedPermission
from core.serializers import UserCreateSerializer, UserSerializer
from core.viewsets import TenantScopedViewSet
from platforms.models import AuditLog, Membership, PlatformSetting, Project, Tenant
from platforms.serializers import (
    AuditLogSerializer,
    MembershipSerializer,
    PlatformSettingSerializer,
    ProjectSerializer,
    TenantSerializer,
)
from platforms.services import AuditService, require_membership


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [TenantScopedPermission]
    permission_required = "platform.manage"
    queryset = Tenant.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or getattr(user, "is_platform_admin", False):
            return qs
        from platforms.models import Membership

        tenant_ids = Membership.objects.filter(user=user, is_active=True).values_list("tenant_id", flat=True)
        return qs.filter(id__in=tenant_ids)

    def perform_destroy(self, instance):
        from platforms.services import purge_tenant_data

        purge_tenant_data(instance)


class ProjectViewSet(TenantScopedViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "platform.manage"
    tenant_field = "tenant_id"
    queryset = Project.objects.select_related("tenant").all()

    def get_queryset(self):
        qs = super().get_queryset()
        tenant_id = self.request.query_params.get("tenant")
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        return qs

    def perform_create(self, serializer):
        tenant = serializer.validated_data.get("tenant")
        if tenant is None:
            from core.errors import ValidationError

            raise ValidationError("tenant is required to create a project.")
        require_membership(self.request.user, tenant, "platform.manage")
        project = serializer.save(tenant=tenant)
        AuditService.record(
            actor=self.request.user,
            action="project.create",
            resource_type="project",
            resource_id=str(project.id),
            tenant=tenant,
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        project = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="project.update",
            resource_type="project",
            resource_id=str(project.id),
            tenant=project.tenant,
        )


class MembershipViewSet(TenantScopedViewSet):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "platform.manage"
    tenant_field = "tenant_id"
    queryset = Membership.objects.select_related("tenant", "role", "user").all()


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    queryset = AuditLog.objects.select_related("tenant", "project", "actor").all()
    tenant_field = "tenant_id"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or getattr(user, "is_platform_admin", False):
            return qs
        from platforms.models import Membership

        tenant_ids = Membership.objects.filter(user=user, is_active=True).values_list("tenant_id", flat=True)
        return qs.filter(tenant_id__in=tenant_ids)


class PlatformSettingViewSet(TenantScopedViewSet):
    serializer_class = PlatformSettingSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "platform.manage"
    tenant_field = "tenant_id"
    queryset = PlatformSetting.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    """User directory for the Administración screen (platform admin only)."""

    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "platform.manage"
    queryset = get_user_model().objects.all().order_by("email")

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="user.create",
            resource_type="user",
            resource_id=str(user.id),
        )

    def perform_update(self, serializer):
        serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="user.update",
            resource_type="user",
            resource_id=str(serializer.instance.id),
        )

    def perform_destroy(self, instance):
        # Users are deactivated, never hard-deleted (audit/history integrity).
        instance.is_active = False
        instance.save(update_fields=["is_active"])
        AuditService.record(
            actor=self.request.user,
            action="user.deactivate",
            resource_type="user",
            resource_id=str(instance.id),
        )
