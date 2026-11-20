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


def test_device_binding_autodiscovery(api, tenant, project, platform_admin):
    from assets.models import Asset, AssetAttribute
    from connectivity.models import Gateway, GatewayBinding
    from telemetry.models import AttributeCurrent

    api.force_authenticate(user=platform_admin)
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")
    gw_asset = Asset.objects.create(
        tenant=tenant, project=project, name="GW", external_ref="gw", asset_type_id=mqtt_type["id"]
    )
    gateway = Gateway.objects.create(
        tenant=tenant,
        project=project,
        asset=gw_asset,
        protocol="mqtt",
        config={"host": "x", "port": 1883, "auto_discover": True, "auto_accept": False},
    )
    device = Asset.objects.create(tenant=tenant, project=project, name="Sensor", external_ref="sensor")
    GatewayBinding.objects.create(
        tenant=tenant,
        project=project,
        gateway=gateway,
        binding_type="device",
        asset=device,
        address="z2m/SN-PRES-01",
    )

    results = process_message(str(gateway.id), "z2m/SN-PRES-01", b'{"temperature": 22.5, "battery": 90}')
    # auto_accept=False: attributes are discovered but NOT ingested while inactive.
    assert not results

    temperature = AssetAttribute.objects.get(asset=device, code="temperature")
    assert temperature.auto_discovered is True
    assert temperature.is_active is False  # auto_accept=False
    assert temperature.value_type == "number"

    # Inactive discovered attributes are NOT ingested.
    assert not AttributeCurrent.objects.filter(attribute_id=temperature.id).exists()

    # Enable and re-send: value is ingested and current updated.
    temperature.is_active = True
    temperature.save(update_fields=["is_active"])
    process_message(str(gateway.id), "z2m/SN-PRES-01", b'{"temperature": 22.5, "battery": 90}')
    current = AttributeCurrent.objects.get(attribute_id=temperature.id)
    assert current.typed_value == 22.5


def test_asset_connectivity_status(tenant, project, platform_admin):
    from assets.models import Asset
    from connectivity.models import Gateway
    from connectivity.services import asset_connectivity_status

    plain = Asset.objects.create(tenant=tenant, project=project, name="Plain", external_ref="plain")
    assert asset_connectivity_status(plain)["status"] == "no_gateway"

    gw_asset = Asset.objects.create(tenant=tenant, project=project, name="GW", external_ref="gw2")
    Gateway.objects.create(tenant=tenant, project=project, asset=gw_asset, protocol="mqtt", config={})
    from connectivity.models import GatewayBinding

    GatewayBinding.objects.create(
        tenant=tenant, project=project, gateway=Gateway.objects.get(asset=gw_asset), asset=plain, address="t"
    )
    assert asset_connectivity_status(plain)["status"] == "disconnected"


def test_adapter_registry_covers_all_protocols():
    from connectivity.adapters.registry import ADAPTERS

    assert set(ADAPTERS) == {"mqtt", "modbus-rtu", "modbus-tcp", "opcua", "bacnet", "snmp", "can"}
    for adapter in set(ADAPTERS.values()):
        assert hasattr(adapter, "run_forever")
        assert hasattr(adapter, "test")


def test_test_connection_delegates_to_adapter(tenant, project, platform_admin):
    from assets.models import Asset
    from connectivity.adapters.bacnet import BacnetAdapter
    from connectivity.models import Gateway
    from connectivity.services import test_gateway_connection

    gw_asset = Asset.objects.create(tenant=tenant, project=project, name="GW-BAC", external_ref="gw-bac")
    gateway = Gateway.objects.create(tenant=tenant, project=project, asset=gw_asset, protocol="bacnet", config={})

    original = BacnetAdapter.test
    BacnetAdapter.test = classmethod(lambda cls, gw: {"status": "connected"})  # type: ignore[method-assign]
    try:
        result = test_gateway_connection(gateway)
    finally:
        BacnetAdapter.test = original
    assert result["status"] == "connected"
    gateway.refresh_from_db()
    assert gateway.connection_status == "connected"


def test_test_connection_adapter_error_marks_status(tenant, project, platform_admin):
    from assets.models import Asset
    from connectivity.adapters.bacnet import BacnetAdapter
    from connectivity.models import Gateway
    from connectivity.services import test_gateway_connection

    gw_asset = Asset.objects.create(tenant=tenant, project=project, name="GW-BAC2", external_ref="gw-bac2")
    gateway = Gateway.objects.create(tenant=tenant, project=project, asset=gw_asset, protocol="bacnet", config={})

    original = BacnetAdapter.test
    BacnetAdapter.test = classmethod(lambda cls, gw: {"status": "error", "detail": "boom"})  # type: ignore[method-assign]
    try:
        result = test_gateway_connection(gateway)
    finally:
        BacnetAdapter.test = original
    assert result["status"] == "error"
    gateway.refresh_from_db()
    assert gateway.connection_status == "error"


def test_modbus_register_parsing():
    from connectivity.adapters.modbus import ModbusAdapter

    assert ModbusAdapter._parse_register("40001") == 40001
    assert ModbusAdapter._parse_register("holding:7") == 7


def test_can_signal_decode():
    from connectivity.adapters.can import CanAdapter

    data = (12345).to_bytes(2, "little")
    assert CanAdapter._decode(data, {"start": 0, "length": 16, "scale": 0.1}) == 1234.5
    assert CanAdapter._decode(data, {"start": 0, "length": 16, "scale": 1, "offset": 5}) == 12350.0


def test_binding_address_sanitized(api, tenant, project, platform_admin):
    api.force_authenticate(user=platform_admin)
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")
    create = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "GW-Clean",
            "external_ref": "gw-clean",
            "asset_type": mqtt_type["id"],
            "gateway_config": {"host": "x", "port": 1883},
        },
        format="json",
    )
    gateway_id = create.data["gateway_id"]
    attr = api.post(
        "/api/v1/assets/attributes/",
        {"asset": create.data["id"], "code": "temp", "name": "temp", "value_type": "number"},
        format="json",
    )
    binding = api.post(
        "/api/v1/connectivity/bindings/",
        {
            "gateway": gateway_id,
            "asset": create.data["id"],
            "attribute": attr.data["id"],
            "address": "z2m-tg/SN-PRES-01\u0000",
        },
        format="json",
    )
    assert binding.status_code == 201, binding.data
    assert binding.data["address"] == "z2m-tg/SN-PRES-01"


def test_gateway_config_strips_control_chars(api, tenant, project, platform_admin):
    from connectivity.models import Gateway

    api.force_authenticate(user=platform_admin)
    type_resp = api.get("/api/v1/assets/types/?kind=gateway")
    mqtt_type = next(r for r in type_resp.data["results"] if r["code"] == "gateway-mqtt")
    create = api.post(
        "/api/v1/assets/assets/",
        {
            "tenant": str(tenant.id),
            "project": str(project.id),
            "name": "GW-Ctrl",
            "external_ref": "gw-ctrl",
            "asset_type": mqtt_type["id"],
            "gateway_config": {"host": "x", "port": 1883, "client_id": "or-domah-bms-01\u0000"},
        },
        format="json",
    )
    assert create.status_code == 201, create.data
    gateway = Gateway.objects.get(id=create.data["gateway_id"])
    assert gateway.config["client_id"] == "or-domah-bms-01"


def test_test_connection_waits_for_connack(monkeypatch, tenant, project, platform_admin):
    import sys
    import time
    import types

    from assets.models import Asset
    from connectivity.models import Gateway
    from connectivity.services import test_gateway_connection

    gw_asset = Asset.objects.create(tenant=tenant, project=project, name="GW-T", external_ref="gw-t")

    class FakeClient:
        def __init__(self, *a, **kw):
            self.calls = 0

        def username_pw_set(self, *a):
            pass

        def tls_set(self):
            pass

        def connect(self, *a, **kw):
            pass

        def loop_start(self):
            pass

        def loop_stop(self):
            pass

        def disconnect(self):
            pass

        def is_connected(self):
            self.calls += 1
            return self.calls >= 2

    paho = types.ModuleType("paho")
    paho_mqtt = types.ModuleType("paho.mqtt")
    client_mod = types.ModuleType("paho.mqtt.client")
    client_mod.Client = FakeClient
    client_mod.CallbackAPIVersion = types.SimpleNamespace(VERSION2=2)
    paho_mqtt.client = client_mod
    monkeypatch.setitem(sys.modules, "paho", paho)
    monkeypatch.setitem(sys.modules, "paho.mqtt", paho_mqtt)
    monkeypatch.setitem(sys.modules, "paho.mqtt.client", client_mod)
    monkeypatch.setattr(time, "sleep", lambda *a, **kw: None)
    monkeypatch.setattr(time, "time", lambda: 0.0)

    gateway = Gateway.objects.create(
        tenant=tenant, project=project, asset=gw_asset, protocol="mqtt", config={"host": "x", "port": 1883}
    )
    result = test_gateway_connection(gateway)
    assert result["status"] == "connected"
    gateway.refresh_from_db()
    assert gateway.connection_status == "connected"
