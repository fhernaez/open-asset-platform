"""Shared pytest configuration. Unit tests run on an in-memory SQLite database
(a test double); integration tests against real PostgreSQL run via Docker (see
``scripts/gates`` and the compose stack)."""

from __future__ import annotations

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["DB_ENGINE"] = "sqlite"

import pytest  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from rest_framework.test import APIClient  # noqa: E402


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture(autouse=True)
def _enable_db_for_all(db):
    pass


@pytest.fixture
def platform_admin(db):
    user_model = get_user_model()
    return user_model.objects.create_user(
        email="admin@example.com",
        password="admin-pass-123",
        is_staff=True,
        is_platform_admin=True,
        is_superuser=True,
    )


@pytest.fixture
def tenant(db):
    from platforms.models import Tenant

    return Tenant.objects.create(name="Test Tenant", slug="test")


@pytest.fixture
def project(db, tenant):
    from platforms.models import Project

    return Project.objects.create(tenant=tenant, name="Site A", code="site-a")


@pytest.fixture
def tenant_admin_role(db):
    from core.models import Role

    return Role.objects.create(slug="tenant_admin", name="Tenant admin", permissions=["*"])


@pytest.fixture
def member_user(db, tenant, tenant_admin_role):
    from core.models import Role
    from platforms.models import Membership

    role, _ = Role.objects.get_or_create(slug="tenant_admin", defaults={"name": "Tenant admin", "permissions": ["*"]})
    user = get_user_model().objects.create_user(email="member@example.com", password="pass-12345")
    Membership.objects.create(user=user, tenant=tenant, role=role, is_active=True)
    return user


@pytest.fixture
def asset(db, tenant, project):
    from assets.models import Asset

    return Asset.objects.create(tenant=tenant, project=project, name="AHU-01", external_ref="AHU-01")


@pytest.fixture
def attribute_factory(db, asset, tenant, project):
    from assets.models import AssetAttribute

    def _make(code, value_type="number", **kwargs):
        kwargs.setdefault("storage_datapoint", True)
        kwargs.setdefault("history_enabled", True)
        return AssetAttribute.objects.create(
            tenant=tenant,
            project=project,
            asset=asset,
            code=code,
            name=code,
            value_type=value_type,
            **kwargs,
        )

    return _make
