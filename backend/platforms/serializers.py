from __future__ import annotations

from rest_framework import serializers

from platforms.models import AuditLog, Membership, PlatformSetting, Project, Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "name", "slug", "timezone", "locale", "is_active", "settings", "created_at"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "tenant", "name", "code", "description", "lifecycle_status", "timezone", "created_at"]
        read_only_fields = ["tenant"]


class MembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Membership
        fields = ["id", "user", "user_email", "tenant", "role", "is_active", "created_at"]
        read_only_fields = ["tenant"]


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "tenant", "project", "actor", "action", "resource_type", "resource_id", "payload", "created_at"]


class PlatformSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformSetting
        fields = ["id", "tenant", "key", "value", "source", "is_mutable", "updated_at"]
