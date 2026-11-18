from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "full_name",
            "is_active",
            "is_platform_admin",
            "locale",
            "timezone",
        ]
        read_only_fields = ["is_platform_admin"]


class UserCreateSerializer(serializers.ModelSerializer):
    """User creation (platform admin): initial password + optional membership."""

    password = serializers.CharField(write_only=True, required=True)
    tenant = serializers.UUIDField(required=False, allow_null=True, write_only=True)
    role = serializers.SlugField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "full_name", "password", "locale", "timezone", "is_active", "tenant", "role"]

    def validate_email(self, value):
        return value.lower()

    def create(self, validated_data):
        from core.models import Role
        from platforms.models import Membership, Tenant

        tenant_id = validated_data.pop("tenant", None)
        role_slug = validated_data.pop("role", None)
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        user = get_user_model().objects.create_user(email=email, password=password, **validated_data)
        if tenant_id:
            tenant = Tenant.objects.get(id=tenant_id)
            role = Role.objects.filter(slug=role_slug).first() if role_slug else None
            if role is not None:
                Membership.objects.create(user=user, tenant=tenant, role=role, is_active=True)
        return user


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token
