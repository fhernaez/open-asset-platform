"""Connectivity services: config validation, topic matching, direct ingest."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from assets.models import AssetAttribute
from connectivity.jsonpath import extract
from connectivity.models import Gateway, GatewayBinding
from core.errors import NotFoundError, ValidationError

logger = logging.getLogger(__name__)


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
        known = {f.get("field") for f in schema} | {"storage_policy"}
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


def process_message(gateway_id: str, topic: str, payload: bytes | str, *, source_event_id: str = "") -> list[dict]:
    """Deliver a message to every binding of a gateway whose address matches."""
    from telemetry.storage import ingest_event

    try:
        gateway = Gateway.objects.select_related("asset__asset_type").get(id=gateway_id)
    except Gateway.DoesNotExist:
        raise NotFoundError("Gateway not found.") from None

    decoded = _decode_payload(payload)
    bindings = GatewayBinding.objects.select_related("asset", "attribute").filter(gateway=gateway)
    matched = [b for b in bindings if topic_matches(b.address, topic)]
    results = []
    storage_policy = (gateway.config or {}).get("storage_policy")

    for binding in matched:
        value = extract(decoded, binding.mapping) if binding.mapping else decoded
        if value is None:
            continue
        attribute = binding.attribute
        result = ingest_event(
            tenant_id=str(gateway.tenant_id),
            project_id=str(gateway.project_id) if gateway.project_id else None,
            asset_id=str(binding.asset_id),
            attribute_id=str(attribute.id),
            value=value,
            value_type=attribute.value_type,
            observed_at=datetime.now(timezone.utc),
            quality="good",
            source_event_id=source_event_id,
            transport="mqtt",
            topic=topic,
            agent_default_policy=storage_policy or None,
            history_enabled=attribute.history_enabled,
            history_override=attribute.history_policy_override,
        )
        results.append({"attribute_id": str(attribute.id), "counters": result.as_dict()})
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
