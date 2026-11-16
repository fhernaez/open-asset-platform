"""Platform bounded context: tenants, projects, membership, audit, settings."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from core.models import UUIDPkModel


class Tenant(UUIDPkModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80, unique=True)
    timezone = models.CharField(max_length=64, default="UTC")
    locale = models.CharField(max_length=16, default="en")
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "platform_tenant"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Project(UUIDPkModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=80)
    description = models.TextField(blank=True, default="")
    lifecycle_status = models.CharField(
        max_length=20,
        choices=[("draft", "Draft"), ("active", "Active"), ("archived", "Archived")],
        default="draft",
    )
    timezone = models.CharField(max_length=64, default="UTC")

    class Meta:
        db_table = "platform_project"
        unique_together = [("tenant", "code")]
        ordering = ["name"]
        indexes = [models.Index(fields=["tenant_id", "id"])]

    def __str__(self) -> str:
        return f"{self.tenant.slug}/{self.code}"


class TenantScopedModel(UUIDPkModel):
    """Abstract base for entities owned by a tenant (and optionally a project)."""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="+")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="+")

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["tenant_id", "project_id", "id"])]


class Membership(UUIDPkModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="memberships")
    role = models.ForeignKey("core.Role", on_delete=models.PROTECT, related_name="+")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "platform_membership"
        unique_together = [("user", "tenant")]
        indexes = [models.Index(fields=["tenant_id", "user_id"])]

    def __str__(self) -> str:
        return f"{self.user.email}@{self.tenant.slug}:{self.role.slug}"


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="audit_logs")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="audit_logs")
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs"
    )
    action = models.CharField(max_length=120)
    resource_type = models.CharField(max_length=80)
    resource_id = models.CharField(max_length=80, blank=True, default="")
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "platform_auditlog"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action} {self.resource_type}"


class PlatformSetting(UUIDPkModel):
    """GUI-persisted settings that outlive environment defaults (seed-once)."""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    key = models.CharField(max_length=120)
    value = models.JSONField(default=dict, blank=True)
    source = models.CharField(max_length=10, choices=[("env", "env"), ("db", "db")], default="db")
    is_mutable = models.BooleanField(default=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        db_table = "platform_platformsetting"
        unique_together = [("tenant", "key")]
