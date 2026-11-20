"""Designations (81346), location assets and manifest rules (ADR-017/018)."""

from __future__ import annotations

from assets.models import Asset, AssetType


def test_set_designation_versions_and_auto_occurrence(tenant, project):
    from assets.services import set_designation

    asset = Asset.objects.create(tenant=tenant, project=project, name="CH-A", external_ref="CH-A")
    first = set_designation(asset, "function", "E1")
    assert first["function"] == {"code": "E1", "occurrence": 1}
    assert first["version"] == 1

    second = set_designation(asset, "function", "E1")
    assert second["function"] == {"code": "E1", "occurrence": 2}
    assert second["version"] == 2
    assert len(second["history"]) == 1
    assert second["history"][0]["occurrence"] == 1
    assert second["history"][0]["until"] == 2

    other = set_designation(asset, "location", "++1")
    assert other["location"] == {"code": "++1", "occurrence": 1}
    assert other["version"] == 3


def test_designation_endpoint(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    asset = Asset.objects.create(tenant=tenant, project=project, name="CH-B", external_ref="CH-B")
    resp = api.post(
        f"/api/v1/assets/assets/{asset.id}/designation/",
        {"aspect": "function", "code": "E2"},
        format="json",
    )
    assert resp.status_code == 200
    assert resp.data["function"] == {"code": "E2", "occurrence": 1}

    bad = api.post(
        f"/api/v1/assets/assets/{asset.id}/designation/",
        {"aspect": "bogus", "code": "X"},
        format="json",
    )
    assert bad.status_code in (400, 422)


def test_manifest_required_attribute_blocks_create(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    asset_type = AssetType.objects.create(
        tenant=tenant,
        project=project,
        code="pump-rules",
        name="Pump Rules",
        kind="asset",
        schema={"rules": {"required_attributes": ["pressure"]}},
    )
    resp = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "PU-1",
            "external_ref": "PU-1",
            "asset_type": str(asset_type.id),
        },
        format="json",
    )
    assert resp.status_code in (400, 422)
    assert "pressure" in str(resp.data)


def test_manifest_required_attribute_satisfied_by_template(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    asset_type = AssetType.objects.create(
        tenant=tenant,
        project=project,
        code="pump-rules2",
        name="Pump Rules 2",
        kind="asset",
        schema={
            "rules": {"required_attributes": ["pressure"]},
            "attributes": [{"code": "pressure", "name": "Pressure", "value_type": "number"}],
        },
    )
    resp = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "PU-2",
            "external_ref": "PU-2",
            "asset_type": str(asset_type.id),
        },
        format="json",
    )
    assert resp.status_code == 201
    from assets.models import AssetAttribute

    assert AssetAttribute.objects.filter(asset_id=resp.data["id"], code="pressure").exists()


def test_location_asset_fields_roundtrip(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    location_type = AssetType.objects.create(
        tenant=tenant,
        project=project,
        code="building-test",
        name="Building",
        kind="standard",
        is_location=True,
        schema={"designation_prefix": "++"},
    )
    resp = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "ED-A",
            "external_ref": "ED-A",
            "asset_type": str(location_type.id),
            "latitude": -31.4,
            "longitude": -64.18,
            "rel_x": 12.5,
            "rel_y": 8.0,
            "geofence": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
            },
        },
        format="json",
    )
    assert resp.status_code == 201, resp.data
    assert resp.data["rel_x"] == 12.5
    assert resp.data["rel_y"] == 8.0
    assert resp.data["geofence"]["type"] == "Polygon"
    location_type.refresh_from_db()
    assert location_type.is_location is True
