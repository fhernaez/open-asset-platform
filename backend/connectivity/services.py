"""Connectivity services: config validation, topic matching, direct ingest.

Gateway messages are routed by binding type (ADR-014 v2):
- attribute: address -> concrete attribute (+ mapping).
- device: address -> device asset; each payload key maps to an attribute by
  code; unknown keys become auto_discovered candidates per gateway config.
Only active attributes are ingested; the configurable storage policy
(on_change + N/window) applies to manual and discovered attributes alike.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from assets.models import Asset, AssetAttribute
from connectivity.jsonpath import extract
from connectivity.models import Gateway, GatewayBinding
from core.errors import NotFoundError, ValidationError

logger = logging.getLogger(__name__)

MAX_DISCOVERED_PER_DEVICE = 200


def _gateway_connection_schema(gateway: Gateway) -> list[dict]:
    asset = gateway.asset
    asset_type = asset.asset_type
    if asset_type is None:
        return []
    return (asset_type.schema or {}).get("connection_schema", [])


def validate_gateway_config(gateway: Gateway, config: dict | None = None) -> list[str]:
    """Validate config against the gateway type's connection_schema."""
    schema = _gateway_connection_schema(gateway)
    if not schema:
        return []
    errors: list[str] = []
    config = config if config is not None else gateway.config
    for field in schema:
        name = field.get("field")
        value = config.get(name) if isinstance(config, dict) else None
        if field.get("required") and (value is None or value == ""):
            errors.append(f"field '{name}' is required.")
            continue
        if value is None:
            continue
        type_ = field.get("type")
        if type_ == "int" and not isinstance(value, int):
            errors.append(f"field '{name}' must be an integer.")
        elif type_ == "bool" and not isinstance(value, bool):
            errors.append(f"field '{name}' must be a boolean.")
        elif type_ in {"string", "secret"} and not isinstance(value, str):
            errors.append(f"field '{name}' must be a string.")
        elif type_ == "select":
            options = [o.get("value") for o in field.get("options", [])]
            if options and value not in options:
                errors.append(f"field '{name}' must be one of {options}.")
    if isinstance(config, dict):
        known = {f.get("field") for f in schema} | {"storage_policy", "auto_discover", "auto_accept"}
        for key in config:
            if key not in known:
                errors.append(f"unknown field '{key}'.")
    return errors


def topic_matches(pattern: str, topic: str) -> bool:
    """MQTT wildcard match: '+' one level, '#' any remaining levels."""
    if "#" in pattern:
        prefix = pattern.split("#", 1)[0].rstrip("/")
        if prefix:
            return topic == prefix or topic.startswith(prefix + "/")
        return True
    pattern_parts = pattern.split("/")
    topic_parts = topic.split("/")
    if len(pattern_parts) != len(topic_parts):
        return False
    for p, t in zip(pattern_parts, topic_parts, strict=False):
        if p not in {"+", t}:
            return False
    return True


def _decode_payload(payload: bytes | str) -> Any:
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return payload
    return payload


def infer_value_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int | float):
        return "number"
    if isinstance(value, dict | list):
        return "json"
    return "string"


def _resolve_device_attribute(
    device: Asset, key: str, gateway: Gateway, auto_discover: bool, auto_accept: bool, sample: Any
):
    code = str(key)[:120]
    attribute = AssetAttribute.objects.filter(asset=device, code=code).first()
    if attribute is not None:
        return attribute
    if not auto_discover:
        return None
    count = AssetAttribute.objects.filter(asset=device, auto_discovered=True).count()
    if count >= MAX_DISCOVERED_PER_DEVICE:
        return None
    attribute = AssetAttribute.objects.create(
        tenant=device.tenant,
        project=device.project,
        asset=device,
        name=code,
        code=code,
        value_type=infer_value_type(sample),
        storage_datapoint=True,
        history_enabled=True,
        auto_discovered=True,
        is_active=bool(auto_accept),
    )
    return attribute


def _ingest(
    binding: GatewayBinding,
    attribute: AssetAttribute,
    value: Any,
    gateway: Gateway,
    topic: str,
    source_event_id: str,
    transport: str = "mqtt",
):
    from telemetry.storage import ingest_event

    return ingest_event(
        tenant_id=str(gateway.tenant_id),
        project_id=str(gateway.project_id) if gateway.project_id else None,
        asset_id=str(binding.asset_id),
        attribute_id=str(attribute.id),
        value=value,
        value_type=attribute.value_type,
        observed_at=datetime.now(timezone.utc),
        quality="good",
        source_event_id=source_event_id,
        transport=transport,
        topic=topic,
        agent_default_policy=(gateway.config or {}).get("storage_policy"),
        history_enabled=attribute.history_enabled,
        history_override=attribute.history_policy_override,
    )


def process_message(gateway_id: str, topic: str, payload: bytes | str, *, source_event_id: str = "") -> list[dict]:
    """Deliver a message to every binding of a gateway whose address matches."""
    try:
        gateway = Gateway.objects.select_related("asset__asset_type").get(id=gateway_id)
    except Gateway.DoesNotExist:
        raise NotFoundError("Gateway not found.") from None

    decoded = _decode_payload(payload)
    bindings = GatewayBinding.objects.select_related("asset", "attribute").filter(gateway=gateway)
    matched = [b for b in bindings if topic_matches(b.address, topic)]
    if not matched:
        return []

    config = gateway.config or {}
    auto_discover = bool(config.get("auto_discover", False))
    auto_accept = bool(config.get("auto_accept", False))
    results: list[dict] = []

    for binding in matched:
        if binding.binding_type == "attribute":
            value = extract(decoded, binding.mapping) if binding.mapping else decoded
            if value is None or binding.attribute is None or not binding.attribute.is_active:
                continue
            result = _ingest(binding, binding.attribute, value, gateway, topic, source_event_id)
            results.append({"attribute_id": str(binding.attribute.id), "counters": result.as_dict()})
            continue

        # Device binding: map payload keys to device attributes.
        scope = extract(decoded, binding.mapping) if binding.mapping else decoded
        if not isinstance(scope, dict):
            continue
        device = binding.asset
        for key, value in scope.items():
            attribute = _resolve_device_attribute(device, key, gateway, auto_discover, auto_accept, value)
            if attribute is None or not attribute.is_active:
                continue
            result = _ingest(binding, attribute, value, gateway, topic, source_event_id)
            results.append(
                {
                    "attribute_id": str(attribute.id),
                    "auto_discovered": attribute.auto_discovered,
                    "counters": result.as_dict(),
                }
            )
    return results


def resolve_effective_policy(attribute: AssetAttribute, gateway: Gateway) -> dict:
    from telemetry.storage import effective_policy

    return effective_policy(
        attribute.history_enabled,
        (gateway.config or {}).get("storage_policy"),
        attribute.history_policy_override,
    )


def ensure_gateway_asset_kind(gateway: Gateway) -> None:
    asset_type = gateway.asset.asset_type
    if asset_type is None or asset_type.kind != "gateway":
        raise ValidationError("Gateway asset must have an asset type of kind 'gateway'.")


def test_gateway_connection(gateway: Gateway) -> dict:
    """Attempt a REAL connection for the gateway protocol."""
    if gateway.protocol != "mqtt":
        return {"status": "not_implemented", "detail": f"adapter '{gateway.protocol}' aún no implementado."}
    config = gateway.config or {}
    host = config.get("host")
    if not host:
        Gateway.objects.filter(id=gateway.id).update(connection_status="error")
        return {"status": "error", "detail": "host is required."}
    port = int(config.get("port") or 1883)
    try:
        import time  # noqa: PLC0415

        import paho.mqtt.client as mqtt  # noqa: PLC0415

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"oap-test-{gateway.id}")
        username = config.get("username")
        if username:
            client.username_pw_set(username, config.get("password"))
        if config.get("tls"):
            client.tls_set()
        client.connect(host, port, keepalive=5)
        client.loop_start()
        # The MQTT CONNACK arrives asynchronously: wait for it briefly.
        deadline = time.time() + 3.0
        connected = False
        while time.time() < deadline:
            if client.is_connected():
                connected = True
                break
            time.sleep(0.1)
        client.loop_stop()
        client.disconnect()
    except Exception as exc:  # noqa: BLE001
        Gateway.objects.filter(id=gateway.id).update(connection_status="error")
        return {"status": "error", "detail": str(exc)[:200]}
    status = "connected" if connected else "error"
    Gateway.objects.filter(id=gateway.id).update(connection_status=status)
    return {"status": status}


def asset_connectivity_status(asset: Asset) -> dict:
    bindings = GatewayBinding.objects.filter(asset=asset).select_related("gateway")
    if not bindings.exists():
        return {"asset_id": str(asset.id), "status": "no_gateway"}
    statuses = {b.gateway.connection_status for b in bindings}
    if "connected" in statuses:
        return {"asset_id": str(asset.id), "status": "connected"}
    if "error" in statuses:
        return {"asset_id": str(asset.id), "status": "error"}
    return {"asset_id": str(asset.id), "status": "disconnected"}
