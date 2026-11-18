"""Connectivity: gateways as assets, bindings, direct MQTT ingest (no Node-RED)."""

from __future__ import annotations

import pytest

from connectivity.models import Gateway, GatewayBinding
from connectivity.services import process_message, topic_matches, validate_gateway_config
from telemetry.models import TelemetryPoint


@pytest.fixture
def gateway_setup(db, tenant, project, asset, attribute_factory, platform_admin):
    from assets.models import AssetType

    attr = attribute_factory("temp")
    gateway_type = AssetType.objects.create(
        tenant=tenant,
        project=project,
        code="gw-mqtt",
        name="Gateway MQTT",
        kind="gateway",
        schema={
            "connection_schema": [
                {"field": "host", "label_i18n": {"es": "Host", "en": "Host"}, "type": "string", "required": True},
                {
                    "field": "port",
                    "label_i18n": {"es": "Puerto", "en": "Port"},
                    "type": "int",
                    "required": True,
                    "default": 1883,
                },
            ]
        },
    )
    from assets.models import Asset

    gateway_asset = Asset.objects.create(
        tenant=tenant,
        project=project,
        name="GW-1",
        external_ref="GW-1",
        asset_type=gateway_type,
    )
    gateway = Gateway.objects.create(
        tenant=tenant,
        project=project,
        asset=gateway_asset,
        protocol="mqtt",
        config={
            "host": "localhost",
            "port": 1883,
            "storage_policy": {"mode": "on_change", "compare": {"absolute_epsilon": 0}},
        },
    )
    GatewayBinding.objects.create(
        tenant=tenant,
        project=project,
        gateway=gateway,
        asset=asset,
        attribute=attr,
        address="site/a/temp",
        mapping="",
    )
    return gateway, attr


def test_direct_ingest_on_change(gateway_setup):
    gateway, attr = gateway_setup
    for _ in range(100):
        process_message(str(gateway.id), "site/a/temp", b"42")
    history = TelemetryPoint.objects.filter(attribute_id=attr.id).order_by("ts")
    assert history.count() == 1


def test_jsonpath_extraction(gateway_setup):
    gateway, attr = gateway_setup
    GatewayBinding.objects.filter(attribute_id=attr.id).update(mapping="data.temperature")
    process_message(str(gateway.id), "site/a/temp", b'{"data": {"temperature": 21.5}}')
    from telemetry.models import AttributeCurrent

    current = AttributeCurrent.objects.get(attribute_id=attr.id)
    assert current.typed_value == 21.5


def test_topic_wildcards():
    assert topic_matches("site/+/temp", "site/a/temp") is True
    assert topic_matches("site/#", "site/a/b/temp") is True
    assert topic_matches("site/a/temp", "site/a/temp") is True
    assert topic_matches("site/a/temp", "site/b/temp") is False


def test_gateway_config_validation(gateway_setup):
    gateway, _ = gateway_setup
    assert validate_gateway_config(gateway) == []
    bad = {"host": "localhost", "port": "not-an-int", "unknown_field": True}
    errors = validate_gateway_config(gateway, bad)
    assert any("port" in e for e in errors)
    assert any("unknown_field" in e for e in errors)


def test_gateway_requires_gateway_kind(tenant, project, asset, platform_admin):
    from assets.models import Asset

    plain_asset = Asset.objects.create(tenant=tenant, project=project, name="Plain", external_ref="plain")
    gateway = Gateway(tenant=tenant, project=project, asset=plain_asset, protocol="mqtt", config={})
    from connectivity.services import ensure_gateway_asset_kind
    from core.errors import ValidationError

    with pytest.raises(ValidationError):
        ensure_gateway_asset_kind(gateway)


def test_gateway_inline_creation(api, tenant, project, platform_admin):
    from connectivity.models import Gateway
    from platforms.models import AuditLog

    api.force_authenticate(user=platform_admin)
    # gateway-mqtt type is seeded by the catalog.
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")

    create = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "GW-Prod",
            "external_ref": "gw-prod",
            "asset_type": mqtt_type["id"],
            "gateway_config": {"host": "mqtt.local", "port": 1884, "tls": True},
        },
        format="json",
    )
    assert create.status_code == 201, create.data
    assert "gateway_id" in create.data
    gateway = Gateway.objects.get(id=create.data["gateway_id"])
    assert gateway.protocol == "mqtt"
    assert gateway.config == {"host": "mqtt.local", "port": 1884, "tls": True}
    assert AuditLog.objects.filter(action="asset.create").exists()


def test_gateway_inline_invalid_config_rolls_back(api, tenant, project, platform_admin):
    from assets.models import Asset
    from connectivity.models import Gateway

    api.force_authenticate(user=platform_admin)
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")
    before = Asset.objects.filter(tenant=tenant).count()

    create = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "GW-Mal",
            "external_ref": "gw-mal",
            "asset_type": mqtt_type["id"],
            "gateway_config": {"host": "x", "port": "no-int", "bogus": 1},
        },
        format="json",
    )
    assert create.status_code in (400, 422)
    assert Asset.objects.filter(tenant=tenant).count() == before
    assert not Gateway.objects.filter(asset__name="GW-Mal").exists()


def test_gateway_storage_policy_endpoint(api, tenant, project, platform_admin):
    from connectivity.models import Gateway

    api.force_authenticate(user=platform_admin)
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")
    create = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "GW-Policy",
            "external_ref": "gw-policy",
            "asset_type": mqtt_type["id"],
            "gateway_config": {"host": "x", "port": 1883},
        },
        format="json",
    )
    assert create.status_code == 201, create.data
    gateway_id = create.data["gateway_id"]

    put = api.put(
        f"/api/v1/connectivity/gateways/{gateway_id}/storage-policy/",
        {"storage_policy": {"mode": "on_change", "max_samples": {"count": 5, "window": "PT1H"}}},
        format="json",
    )
    assert put.status_code == 200, put.data
    assert put.data["storage_policy"]["mode"] == "on_change"
    gateway = Gateway.objects.get(id=gateway_id)
    assert gateway.config["storage_policy"]["max_samples"]["count"] == 5
