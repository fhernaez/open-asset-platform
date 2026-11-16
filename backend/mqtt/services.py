"""MQTT ingest service: decode payload, extract via JSONPath, drive telemetry."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from assets.models import AssetAttribute
from core.errors import NotFoundError
from mqtt.jsonpath import extract
from mqtt.models import MqttAgent, MqttBinding
from telemetry.storage import effective_policy, ingest_event

logger = logging.getLogger(__name__)


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


def effective_attribute_policy(attribute: AssetAttribute, agent: MqttAgent) -> dict:
    """Merge agent storage defaults with the attribute override."""
    return effective_policy(
        attribute.history_enabled,
        agent.storage_policy_defaults or None,
        attribute.history_policy_override,
    )


def process_message(agent_id: str, topic: str, payload: bytes | str, *, source_event_id: str = "") -> list[dict]:
    """Deliver an MQTT message to every binding of an agent that matches the topic.

    Returns the per-attribute ingest results (counters), or [] when no binding
    matches. This is the direct ingest path; Node-RED is not involved.
    """
    try:
        agent = MqttAgent.objects.select_related("broker").get(id=agent_id)
    except MqttAgent.DoesNotExist:
        raise NotFoundError("MqttAgent not found.") from None

    decoded = _decode_payload(payload)
    bindings = MqttBinding.objects.select_related("asset", "attribute").filter(agent=agent)
    matched = [b for b in bindings if topic_matches(b.subscribe_topic, topic)]
    if not matched:
        return []

    results = []
    for binding in matched:
        value = extract(decoded, binding.json_path) if binding.json_path else decoded
        if value is None:
            continue
        attribute = binding.attribute
        result = ingest_event(
            tenant_id=str(agent.tenant_id),
            project_id=str(agent.project_id) if agent.project_id else None,
            asset_id=str(binding.asset_id),
            attribute_id=str(attribute.id),
            value=value,
            value_type=attribute.value_type,
            observed_at=datetime.now(UTC),
            quality="good",
            source_event_id=source_event_id,
            transport="mqtt",
            topic=topic,
            agent_default_policy=agent.storage_policy_defaults or None,
            history_enabled=attribute.history_enabled,
            history_override=attribute.history_policy_override,
        )
        results.append({"attribute_id": str(attribute.id), "counters": result.as_dict()})
    return results
