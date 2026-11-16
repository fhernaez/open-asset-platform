"""MQTT direct ingest through bindings (no Node-RED)."""

from __future__ import annotations

import pytest

from mqtt.models import BrokerConnection, MqttAgent, MqttBinding
from mqtt.services import process_message
from telemetry.models import TelemetryPoint


@pytest.fixture
def mqtt_setup(db, tenant, project, asset, attribute_factory):
    attr = attribute_factory("temp")
    broker = BrokerConnection.objects.create(tenant=tenant, project=project, name="local", host="localhost", port=1883)
    agent = MqttAgent.objects.create(
        tenant=tenant,
        project=project,
        name="agent-1",
        broker=broker,
        storage_policy_defaults={"mode": "on_change", "compare": {"absolute_epsilon": 0}},
    )
    MqttBinding.objects.create(
        tenant=tenant,
        project=project,
        agent=agent,
        asset=asset,
        attribute=attr,
        subscribe_topic="site/a/temp",
        json_path="",
    )
    return agent, attr


def test_direct_ingest_on_change(mqtt_setup):
    agent, attr = mqtt_setup
    for _ in range(100):
        process_message(str(agent.id), "site/a/temp", b"42")
    history = TelemetryPoint.objects.filter(attribute_id=attr.id).order_by("ts")
    assert history.count() == 1


def test_jsonpath_extraction(mqtt_setup):
    agent, attr = mqtt_setup
    MqttBinding.objects.filter(attribute_id=attr.id).update(json_path="data.temperature")
    process_message(str(agent.id), "site/a/temp", b'{"data": {"temperature": 21.5}}')
    from telemetry.models import AttributeCurrent

    current = AttributeCurrent.objects.get(attribute_id=attr.id)
    assert current.typed_value == 21.5


def test_topic_wildcards(db, tenant, project, asset, attribute_factory):
    from mqtt.services import topic_matches

    assert topic_matches("site/+/temp", "site/a/temp") is True
    assert topic_matches("site/#", "site/a/b/temp") is True
    assert topic_matches("site/a/temp", "site/a/temp") is True
    assert topic_matches("site/a/temp", "site/b/temp") is False
