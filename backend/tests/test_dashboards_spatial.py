"""Dashboards and spatial (scenes/placements) API tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def api():
    from rest_framework.test import APIClient

    return APIClient()


def test_dashboard_crud(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    create = api.post(
        "/api/v1/dashboards/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "Operación", "grid_cols": 12, "grid_rows": 6},
        format="json",
    )
    assert create.status_code == 201, create.data
    dashboard_id = create.data["id"]

    widget = api.post(
        "/api/v1/dashboards/widgets/",
        {
            "dashboard": dashboard_id,
            "title": "Temperatura",
            "widget_type": "line",
            "x": 0,
            "y": 0,
            "w": 6,
            "h": 3,
            "config": {"attribute_ids": []},
        },
        format="json",
    )
    assert widget.status_code == 201, widget.data

    listing = api.get(f"/api/v1/dashboards/?tenant={tenant.id}")
    assert listing.status_code == 200
    assert any(d["name"] == "Operación" for d in listing.data["results"])


def test_scene_and_placement(api, tenant, project, platform_admin):
    from io import BytesIO

    from PIL import Image

    api.force_authenticate(user=platform_admin)
    create = api.post(
        "/api/v1/spatial/scenes/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "Plano planta baja"},
        format="json",
    )
    assert create.status_code == 201, create.data
    scene_id = create.data["id"]

    buffer = BytesIO()
    Image.new("RGB", (10, 10), color="white").save(buffer, format="PNG")
    buffer.seek(0)
    layer = api.post(
        f"/api/v1/spatial/scenes/{scene_id}/layers/",
        {"key": "planta", "name": "Planta", "image": buffer},
        format="multipart",
    )
    assert layer.status_code == 201, layer.data
    layer_id = layer.data["id"]

    asset = api.post(
        "/api/v1/assets/assets/",
        {"tenant": str(tenant.id), "project": str(project.id), "name": "AHU-2", "external_ref": "ahu-2"},
        format="json",
    )
    placement = api.post(
        "/api/v1/spatial/placements/",
        {"scene": scene_id, "layer": layer_id, "asset": asset.data["id"], "x": 0.5, "y": 0.5, "z": 0},
        format="json",
    )
    assert placement.status_code == 201, placement.data

    scene = api.get(f"/api/v1/spatial/scenes/{scene_id}/")
    assert scene.status_code == 200
    assert len(scene.data["layers"]) == 1
    assert len(scene.data["placements"]) == 1


def test_users_readonly(api, platform_admin):
    api.force_authenticate(user=platform_admin)
    listing = api.get("/api/v1/platform/users/")
    assert listing.status_code == 200
    emails = {u["email"] for u in listing.data["results"]}
    assert "admin@example.com" in emails


def test_map_config_bounds(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    put = api.put(
        f"/api/v1/spatial/projects/{project.id}/map-config/",
        {"bounds": {"north": -34.5, "south": -34.7, "east": -58.3, "west": -58.5}},
        format="json",
    )
    assert put.status_code == 200, put.data
    assert put.data["bounds"]["north"] == -34.5

    get = api.get(f"/api/v1/spatial/projects/{project.id}/map-config/")
    assert get.status_code == 200
    assert get.data["bounds"]["west"] == -58.5


def test_purge_project_dry_run(tenant, project, platform_admin):
    from io import StringIO

    from django.core.management import call_command

    from assets.models import Asset

    Asset.objects.create(tenant=tenant, project=project, name="X", external_ref="x")
    out = StringIO()
    call_command("purge_project", code=project.code, stdout=out)
    assert "DRY RUN" in out.getvalue()
    assert Asset.objects.filter(project=project).count() == 1

    call_command("purge_project", code=project.code, yes=True, stdout=out)
    assert Asset.objects.filter(project=project).count() == 0
