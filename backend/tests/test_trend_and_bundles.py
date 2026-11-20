"""Trend endpoint (ADR-019) and dashboard bundles/templates tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from dashboards.models import Dashboard, DashboardTemplate, Widget
from telemetry.storage import ingest_event

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _seed(attribute, count=60, step=10, start_value=1.0):
    for i in range(count):
        ingest_event(
            tenant_id=str(attribute.tenant_id),
            project_id=str(attribute.project_id) if attribute.project_id else None,
            asset_id=str(attribute.asset_id),
            attribute_id=str(attribute.id),
            value=start_value + i,
            value_type="number",
            observed_at=BASE + timedelta(seconds=i * step),
            history_enabled=True,
            agent_default_policy=None,
        )


def test_trend_multi_attribute_avg_downsampling_with_gaps(api, tenant, project, platform_admin, attribute_factory):
    api.force_authenticate(user=platform_admin)
    temp = attribute_factory("trend_temp")
    hum = attribute_factory("trend_hum")
    _seed(temp, count=60, step=10)
    _seed(hum, count=30, step=20)

    resp = api.post(
        "/api/v1/telemetry/trend",
        {
            "attributes": [str(temp.id), str(hum.id)],
            "tenant": str(tenant.id),
            "from": BASE.isoformat(),
            "to": (BASE + timedelta(minutes=20)).isoformat(),
            "interval": "5s",
            "downsample": "avg",
        },
        format="json",
    )
    assert resp.status_code == 200, resp.data
    series = {s["attribute_id"]: s for s in resp.data["series"]}
    assert set(series) == {str(temp.id), str(hum.id)}
    assert series[str(temp.id)]["code"] == "trend_temp"
    buckets = series[str(temp.id)]["points"]
    assert len(buckets) <= 61
    assert all(not p["gap"] for p in buckets[:3])
    gaps = [p for p in series[str(hum.id)]["points"] if p["gap"]]
    assert gaps, "missing data should produce gap flags"


def test_trend_lttb_respects_max_points(api, tenant, project, platform_admin, attribute_factory):
    api.force_authenticate(user=platform_admin)
    attr = attribute_factory("trend_lttb")
    _seed(attr, count=200, step=5)
    resp = api.post(
        "/api/v1/telemetry/trend",
        {"attributes": [str(attr.id)], "tenant": str(tenant.id), "downsample": "lttb", "max_points": 30},
        format="json",
    )
    assert resp.status_code == 200, resp.data
    assert len(resp.data["series"][0]["points"]) == 30


def test_trend_rejects_foreign_attribute(api, tenant, project, platform_admin, member_user, attribute_factory):
    from assets.models import AssetAttribute
    from platforms.models import Project, Tenant

    api.force_authenticate(user=platform_admin)
    attr = attribute_factory("trend_priv")
    foreign = Tenant.objects.create(name="Foreign", slug="foreign")
    foreign_project = Project.objects.create(tenant=foreign, name="Foreign Site", code="foreign-site")
    foreign_attr = AssetAttribute.objects.create(
        tenant=foreign, project=foreign_project, asset=attr.asset, code="trend_foreign",
        name="Foreign", value_type="number",
    )
    # member_user has no membership on the foreign tenant.
    api.force_authenticate(user=member_user)
    resp = api.post(
        "/api/v1/telemetry/trend",
        {"attributes": [str(foreign_attr.id)], "tenant": str(foreign.id)},
        format="json",
    )
    assert resp.status_code == 403


def test_bundle_export_import_roundtrip(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    dashboard = Dashboard.objects.create(tenant=tenant, project=project, name="Ops", grid_cols=24, grid_rows=10)
    Widget.objects.create(
        dashboard=dashboard, title="Trend A", widget_type="trend", x=0, y=0, w=8, h=4, config={"series": []}
    )
    Widget.objects.create(
        dashboard=dashboard, title="Map", widget_type="map", x=8, y=0, w=8, h=6, config={"symbols": ["pump"]}
    )

    export = api.post(
        f"/api/v1/dashboards/{dashboard.id}/export-bundle/",
        {"name": "Ops bundle"},
        format="json",
    )
    assert export.status_code == 201, export.data
    bundle_id = export.data["id"]

    import_resp = api.post(f"/api/v1/dashboards/bundles/{bundle_id}/import/", {}, format="json")
    assert import_resp.status_code == 201, import_resp.data
    new_dashboard = Dashboard.objects.get(id=import_resp.data["id"])
    assert new_dashboard.id != dashboard.id
    assert new_dashboard.grid_cols == 24
    widgets = list(new_dashboard.widgets.all())
    assert len(widgets) == 2
    assert {w.widget_type for w in widgets} == {"trend", "map"}
    assert any(w.config.get("symbols") == ["pump"] for w in widgets)


def test_template_apply_creates_dashboard(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    template = DashboardTemplate.objects.create(
        tenant=tenant,
        project=project,
        name="Plant overview",
        category="energy",
        definition={
            "dashboard": {"name": "Plant overview", "grid_cols": 12},
            "widgets": [{"title": "Power", "widget_type": "line", "x": 0, "y": 0, "w": 6, "h": 3, "config": {}}],
        },
    )
    resp = api.post(
        f"/api/v1/dashboards/templates/{template.id}/apply/",
        {"name": "Plant overview (copy)"},
        format="json",
    )
    assert resp.status_code == 201, resp.data
    dashboard = Dashboard.objects.get(id=resp.data["id"])
    assert dashboard.name == "Plant overview (copy)"
    assert dashboard.widgets.count() == 1


def test_symbols_catalog(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    resp = api.get("/api/v1/dashboards/symbols/")
    assert resp.status_code == 200
    keys = {s["key"] for s in resp.data["symbols"]}
    assert {"pump", "fan", "chiller", "boiler", "valve", "motor", "tank", "sensor", "meter", "generator"} <= keys
