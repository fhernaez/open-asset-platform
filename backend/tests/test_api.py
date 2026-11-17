"""Authentication and tenant-isolation API tests."""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api():
    return APIClient()


def test_login_and_me(api, platform_admin):
    response = api.post(
        "/api/v1/auth/login", {"email": "admin@example.com", "password": "admin-pass-123"}, format="json"
    )
    assert response.status_code == 200
    assert "access" in response.data
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    me = api.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.data["email"] == "admin@example.com"


def test_health_unauthenticated(api):
    response = api.get("/api/v1/health")
    assert response.status_code == 200
    assert response.data["status"] == "ok"


def test_tenant_isolation(api, tenant, project, member_user, tenant_admin_role):
    from assets.models import Asset
    from platforms.models import Membership, Tenant

    other_tenant = Tenant.objects.create(name="Other", slug="other")
    Asset.objects.create(tenant=tenant, project=project, name="A1", external_ref="A1")
    Asset.objects.create(tenant=other_tenant, name="B1", external_ref="B1")

    # member only belongs to `tenant`
    assert Membership.objects.filter(user=member_user, tenant=tenant).exists()

    api.force_authenticate(user=member_user)
    listing = api.get("/api/v1/assets/assets/")
    assert listing.status_code == 200
    names = {r["name"] for r in listing.data["results"]}
    assert "A1" in names
    assert "B1" not in names


def test_asset_crud_audit(api, tenant, project, member_user):
    api.force_authenticate(user=member_user)
    create = api.post(
        "/api/v1/assets/assets/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "Pump-1", "external_ref": "Pump-1"},
        format="json",
    )
    assert create.status_code == 201, create.data
    asset_id = create.data["id"]

    from platforms.models import AuditLog

    assert AuditLog.objects.filter(action="asset.create", resource_id=asset_id).exists()

    attr = api.post(
        "/api/v1/assets/attributes/",
        {
            "asset": asset_id,
            "code": "flow",
            "name": "flow",
            "value_type": "number",
            "storage_datapoint": True,
            "history_enabled": True,
        },
        format="json",
    )
    assert attr.status_code == 201, attr.data


def test_admin_without_membership_creates_asset(api, tenant, project, platform_admin):
    # Regression: the bootstrap admin has no Membership; creation must work when
    # tenant/project are provided explicitly (previous read_only serializer broke this).
    api.force_authenticate(user=platform_admin)
    create = api.post(
        "/api/v1/assets/assets/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "AHU-1", "external_ref": "AHU-1"},
        format="json",
    )
    assert create.status_code == 201, create.data
    assert str(create.data["tenant"]) == str(tenant.id)
    assert str(create.data["project"]) == str(project.id)


def test_admin_creates_tenant_and_project(api, platform_admin):
    api.force_authenticate(user=platform_admin)
    tenant_resp = api.post(
        "/api/v1/platform/tenants/", {"name": "Hotel Demo", "slug": "hotel-demo"}, format="json"
    )
    assert tenant_resp.status_code == 201, tenant_resp.data
    tenant_id = tenant_resp.data["id"]
    project_resp = api.post(
        "/api/v1/platform/projects/",
        {"tenant": tenant_id, "name": "Torre A", "code": "torre-a"},
        format="json",
    )
    assert project_resp.status_code == 201, project_resp.data
    assert str(project_resp.data["tenant"]) == str(tenant_id)
