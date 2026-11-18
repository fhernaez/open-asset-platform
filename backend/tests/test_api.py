"""Authentication and tenant-isolation API tests."""

from __future__ import annotations


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
    tenant_resp = api.post("/api/v1/platform/tenants/", {"name": "Hotel Demo", "slug": "hotel-demo"}, format="json")
    assert tenant_resp.status_code == 201, tenant_resp.data
    tenant_id = tenant_resp.data["id"]
    project_resp = api.post(
        "/api/v1/platform/projects/",
        {"tenant": tenant_id, "name": "Torre A", "code": "torre-a"},
        format="json",
    )
    assert project_resp.status_code == 201, project_resp.data
    assert str(project_resp.data["tenant"]) == str(tenant_id)


def test_asset_type_template_creates_attributes(api, tenant, project, platform_admin):
    from assets.models import AssetAttribute

    api.force_authenticate(user=platform_admin)
    type_resp = api.post(
        "/api/v1/assets/types/",
        {
            "tenant": str(tenant.id),
            "name": "Unidad de tratamiento de aire custom",
            "code": "ahu-custom",
            "kind": "standard",
            "schema": {
                "attributes": [
                    {"code": "temp", "name": "Temperatura", "value_type": "number", "storage_datapoint": True},
                    {"code": "mode", "name": "Modo", "value_type": "string"},
                ]
            },
        },
        format="json",
    )
    assert type_resp.status_code == 201, type_resp.data
    type_id = type_resp.data["id"]

    asset_resp = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "AHU-1",
            "external_ref": "AHU-1",
            "asset_type": type_id,
        },
        format="json",
    )
    assert asset_resp.status_code == 201, asset_resp.data
    asset_id = asset_resp.data["id"]

    codes = sorted(AssetAttribute.objects.filter(asset_id=asset_id).values_list("code", flat=True))
    assert codes == ["mode", "temp"]
    temp = AssetAttribute.objects.get(asset_id=asset_id, code="temp")
    assert temp.storage_datapoint is True


def test_gateway_type_kind(api, tenant, platform_admin):
    api.force_authenticate(user=platform_admin)
    create = api.post(
        "/api/v1/assets/types/",
        {
            "tenant": str(tenant.id),
            "name": "Gateway MQTT custom",
            "code": "gateway-mqtt-custom",
            "kind": "gateway",
            "schema": {},
        },
        format="json",
    )
    assert create.status_code == 201, create.data
    assert create.data["kind"] == "gateway"
    listing = api.get("/api/v1/assets/types/?kind=gateway")
    assert listing.status_code == 200
    kinds = {r["kind"] for r in listing.data["results"]}
    assert kinds == {"gateway"}
    assert any(r["code"] == "gateway-mqtt-custom" for r in listing.data["results"])


def test_delete_asset_purges_telemetry(api, tenant, project, platform_admin):
    from django.utils import timezone

    from assets.models import AssetAttribute
    from telemetry.models import AttributeCurrent, TelemetryPoint
    from telemetry.storage import ingest_event

    api.force_authenticate(user=platform_admin)
    asset_resp = api.post(
        "/api/v1/assets/assets/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "Bomba-1", "external_ref": "bomba-1"},
        format="json",
    )
    assert asset_resp.status_code == 201, asset_resp.data
    asset_id = asset_resp.data["id"]
    attr = AssetAttribute.objects.create(
        tenant=tenant,
        project=project,
        asset_id=asset_id,
        name="presion",
        code="presion",
        value_type="number",
        storage_datapoint=True,
        history_enabled=True,
    )
    ingest_event(
        tenant_id=str(tenant.id),
        project_id=str(project.id),
        asset_id=asset_id,
        attribute_id=str(attr.id),
        value=42,
        value_type="number",
        observed_at=timezone.now(),
        history_enabled=True,
    )
    assert TelemetryPoint.objects.filter(attribute_id=attr.id).count() == 1
    assert AttributeCurrent.objects.filter(attribute_id=attr.id).exists()

    delete = api.delete(f"/api/v1/assets/assets/{asset_id}/")
    assert delete.status_code == 204
    assert TelemetryPoint.objects.filter(attribute_id=attr.id).count() == 0
    assert not AttributeCurrent.objects.filter(attribute_id=attr.id).exists()
    assert not AssetAttribute.objects.filter(id=attr.id).exists()


def test_delete_type_in_use_conflicts(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    type_resp = api.post(
        "/api/v1/assets/types/",
        {"tenant": str(tenant.id), "name": "Tipo en uso", "code": "tipo-en-uso", "kind": "standard", "schema": {}},
        format="json",
    )
    assert type_resp.status_code == 201
    asset_resp = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "Equipo",
            "external_ref": "equipo",
            "asset_type": type_resp.data["id"],
        },
        format="json",
    )
    assert asset_resp.status_code == 201
    delete = api.delete(f"/api/v1/assets/types/{type_resp.data['id']}/")
    assert delete.status_code == 409
    assert "en uso" in str(delete.data.get("detail", ""))


def test_retire_asset_via_patch(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    create = api.post(
        "/api/v1/assets/assets/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "Fan-1", "external_ref": "fan-1"},
        format="json",
    )
    assert create.status_code == 201, create.data
    asset_id = create.data["id"]
    patch = api.patch(f"/api/v1/assets/assets/{asset_id}/", {"status": "retired"}, format="json")
    assert patch.status_code == 200, patch.data
    assert patch.data["status"] == "retired"


def test_user_crud_and_locale(api, tenant, platform_admin, tenant_admin_role):
    api.force_authenticate(user=platform_admin)
    create = api.post(
        "/api/v1/platform/users/",
        {
            "email": "Nuevo@Example.com",
            "full_name": "Nuevo Usuario",
            "password": "inicial-12345",
            "locale": "es",
            "timezone": "America/Argentina/Buenos_Aires",
            "tenant": str(tenant.id),
            "role": "tenant_admin",
        },
        format="json",
    )
    assert create.status_code == 201, create.data
    assert create.data["email"] == "nuevo@example.com"
    user_id = create.data["id"]

    from platforms.models import Membership

    assert Membership.objects.filter(user_id=user_id, tenant=tenant).exists()

    patch = api.patch(f"/api/v1/platform/users/{user_id}/", {"locale": "en", "is_active": False}, format="json")
    assert patch.status_code == 200, patch.data
    assert patch.data["locale"] == "en"
    assert patch.data["is_active"] is False


def test_asset_gateway_binding_on_create(api, tenant, project, platform_admin):
    from connectivity.models import GatewayBinding

    api.force_authenticate(user=platform_admin)
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")
    gw = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "GW-Assoc",
            "external_ref": "gw-assoc",
            "asset_type": mqtt_type["id"],
            "gateway_config": {"host": "x", "port": 1883},
        },
        format="json",
    )
    assert gw.status_code == 201, gw.data

    device = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "Sensor-A",
            "external_ref": "sensor-a",
            "gateway_id": gw.data["gateway_id"],
        },
        format="json",
    )
    assert device.status_code == 201, device.data
    binding = GatewayBinding.objects.get(gateway_id=gw.data["gateway_id"], asset_id=device.data["id"])
    assert binding.binding_type == "device"


def test_assets_kind_filter_hides_gateways(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")
    api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "GW-Kind",
            "external_ref": "gw-kind",
            "asset_type": mqtt_type["id"],
            "gateway_config": {"host": "x", "port": 1883},
        },
        format="json",
    )
    api.post(
        "/api/v1/assets/assets/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "Sensor-Kind", "external_ref": "sensor-kind"},
        format="json",
    )
    listing = api.get(f"/api/v1/assets/assets/?tenant={tenant.id}&kind=non_gateway")
    assert listing.status_code == 200
    names = {r["name"] for r in listing.data["results"]}
    assert "Sensor-Kind" in names
    assert "GW-Kind" not in names


def test_delete_tenant_purges_data(api, tenant, project, platform_admin):
    from platforms.models import Tenant

    api.force_authenticate(user=platform_admin)
    api.post(
        "/api/v1/assets/assets/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "A", "external_ref": "a"},
        format="json",
    )
    delete = api.delete(f"/api/v1/platform/tenants/{tenant.id}/")
    assert delete.status_code == 204
    assert not Tenant.objects.filter(id=tenant.id).exists()
