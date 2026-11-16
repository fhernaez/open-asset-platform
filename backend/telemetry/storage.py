"""Telemetry ingestion pipeline: current -> rules -> storage policy -> history.

Implements the normative contract in ``docs/core/TELEMETRY_POLICY.md``:
persistence is evaluated AFTER current value and rule/alarm observers, and only
accepted samples are written to history. MQTT never requires Node-RED.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from django.conf import settings
from django.db import transaction
from django.db.models import F

from telemetry.models import (
    AttributeCurrent,
    IngestMetrics,
    StoragePolicyState,
    TelemetryPoint,
)
from telemetry.policy import (
    canonical_json,
    is_change,
    normalize_value,
    parse_window,
    window_bucket,
)

_observers: list[Callable[[dict], None]] = []


def subscribe_observer(fn: Callable[[dict], None]) -> None:
    """Register a rule/alarm observer invoked for every valid observed sample."""
    _observers.append(fn)


@dataclass
class IngestResult:
    received: int = 0
    valid: int = 0
    invalid: int = 0
    duplicate: int = 0
    accepted: int = 0
    filtered_equal: int = 0
    filtered_quota: int = 0
    late: int = 0
    current_updated: bool = False

    def as_dict(self) -> dict:
        return {
            "received": self.received,
            "valid": self.valid,
            "invalid": self.invalid,
            "duplicate": self.duplicate,
            "accepted": self.accepted,
            "filtered_equal": self.filtered_equal,
            "filtered_quota": self.filtered_quota,
            "late": self.late,
        }


def _dedupe_key(
    attribute_id: str, source_event_id: str, transport: str, topic: str, sequence, observed_at: str, canonical: str
) -> str:
    if source_event_id:
        return hashlib.sha256(f"id:{source_event_id}".encode()).hexdigest()
    raw = f"{transport}:{topic}:{sequence or ''}:{observed_at}:{canonical}"
    return hashlib.sha256(raw.encode()).hexdigest()


def _policy_hash(policy: dict) -> int:
    raw = canonical_json(policy)
    return int(hashlib.sha256(raw.encode()).hexdigest()[:8], 16)


def _default_policy() -> dict:
    return {
        "mode": settings.TELEMETRY_DEFAULT_STORAGE_MODE,
        "compare": {"absolute_epsilon": settings.TELEMETRY_DEFAULT_ABSOLUTE_EPSILON},
        "max_samples": {
            "count": settings.TELEMETRY_DEFAULT_MAX_SAMPLES,
            "window": settings.TELEMETRY_DEFAULT_WINDOW,
            "strategy": settings.TELEMETRY_DEFAULT_WINDOW_STRATEGY,
        },
    }


def effective_policy(history_enabled: bool, agent_default: dict | None, override: dict | None) -> dict:
    """Resolve the effective storage policy for an attribute."""
    base = dict(agent_default or _default_policy())
    policy = base
    if override:
        policy = {**base, **override}
        for key in ("compare", "max_samples", "heartbeat"):
            if isinstance(override.get(key), dict) and isinstance(base.get(key), dict):
                policy[key] = {**base[key], **override[key]}
    policy["storage_datapoint"] = bool(history_enabled)
    return policy


def ingest_event(
    *,
    tenant_id: str,
    project_id: str | None,
    asset_id: str,
    attribute_id: str,
    value: Any,
    value_type: str,
    observed_at: datetime,
    quality: str = "good",
    source_event_id: str = "",
    sequence: int | None = None,
    transport: str = "mqtt",
    topic: str = "",
    agent_default_policy: dict | None = None,
    history_enabled: bool = True,
    history_override: dict | None = None,
    ingest_time: datetime | None = None,
) -> IngestResult:
    result = IngestResult()
    result.received = 1

    ingest_time = ingest_time or datetime.now(UTC)
    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(tzinfo=UTC)

    norm, valid, canonical = normalize_value(value, value_type)

    # Future-event (clock skew) handling: samples ahead of server time beyond the
    # allowed skew are classified as late and never persisted. Historical samples
    # are accepted normally; watermark-based late rejection is a later refinement.
    max_skew = int(getattr(settings, "TELEMETRY_MAX_CLOCK_SKEW_SECONDS", 300))
    if observed_at > ingest_time + timedelta(seconds=max_skew):
        result.late = 1
        _update_current(
            tenant_id,
            project_id,
            asset_id,
            attribute_id,
            norm,
            valid,
            value_type,
            observed_at,
            quality,
            source_event_id,
        )
        _record_metrics(attribute_id, observed_at, result)
        return result

    # Deduplicate source event (QoS1 replay protection).
    key = _dedupe_key(
        str(attribute_id), source_event_id, transport, topic, sequence, observed_at.isoformat(), canonical
    )
    if TelemetryPoint.objects.filter(attribute_id=attribute_id, dedupe_key=key).exists():
        result.duplicate = 1
        _record_metrics(attribute_id, observed_at, result)
        return result

    # Update current value (last observed + last valid) for every valid/invalid sample.
    _update_current(
        tenant_id, project_id, asset_id, attribute_id, norm, valid, value_type, observed_at, quality, source_event_id
    )
    result.current_updated = True

    if not valid:
        result.invalid = 1
        _record_metrics(attribute_id, observed_at, result)
        return result

    result.valid = 1

    # Rules/alarms observe EVERY valid sample, before the storage filter.
    for observer in _observers:
        observer(
            {
                "tenant_id": tenant_id,
                "project_id": project_id,
                "asset_id": asset_id,
                "attribute_id": attribute_id,
                "value": norm,
                "value_type": value_type,
                "observed_at": observed_at,
                "quality": quality,
            }
        )

    if not history_enabled:
        _record_metrics(attribute_id, observed_at, result)
        return result

    policy = effective_policy(history_enabled, agent_default_policy, history_override)

    try:
        with transaction.atomic():
            state = _lock_state(attribute_id)
            accepted = _apply_policy(
                state,
                attribute_id,
                tenant_id,
                norm,
                value_type,
                observed_at,
                quality,
                key,
                source_event_id,
                sequence,
                policy,
            )
        if accepted == "accepted":
            result.accepted = 1
        elif accepted == "equal":
            result.filtered_equal = 1
        elif accepted == "quota":
            result.filtered_quota = 1
        elif accepted == "min_interval":
            result.filtered_quota = 1
    except Exception:  # noqa: BLE001 - record failure, never crash the pipeline
        result.filtered_equal = 0
        _record_metrics(attribute_id, observed_at, result, failure=True)
        return result

    _record_metrics(attribute_id, observed_at, result)
    return result


def _apply_policy(
    state,
    attribute_id,
    tenant_id,
    norm,
    value_type,
    observed_at,
    quality,
    dedupe_key,
    source_event_id,
    sequence,
    policy,
) -> str:
    """Return 'accepted' | 'equal' | 'quota' | 'min_interval'."""
    mode = policy.get("mode", "on_change")
    compare = policy.get("compare") or {}
    max_samples = policy.get("max_samples") or {}
    n = max_samples.get("count")
    window = max_samples.get("window")
    window_seconds = parse_window(window) if window else None

    if mode == "on_change":
        baseline = state.last_persisted_value
        if not is_change(norm, baseline, value_type, compare):
            return "equal"

    if mode == "min_interval":
        interval = parse_window(policy.get("min_interval") or "1s")
        if state.last_persisted_ts is not None:
            delta = (observed_at - state.last_persisted_ts).total_seconds()
            if delta < interval:
                return "min_interval"

    # Quota enforcement: fixed UTC window, atomic under row lock.
    if window_seconds is not None and n is not None and int(n) >= 1:
        bucket = window_bucket(observed_at, window_seconds)
        if state.quota_bucket != bucket:
            state.quota_bucket = bucket
            state.quota_count = 0
        if state.quota_count >= int(n):
            state.save(update_fields=["quota_bucket", "quota_count"])
            return "quota"
        state.quota_count = state.quota_count + 1

    policy_version = _policy_hash(policy)
    TelemetryPoint.objects.create(
        tenant_id=tenant_id,
        attribute_id=attribute_id,
        ts=observed_at,
        ingested_at=datetime.now(UTC),
        value_type=value_type,
        typed_value=norm,
        quality=quality,
        policy_version=policy_version,
        source_event_id=source_event_id or "",
        dedupe_key=dedupe_key,
        sequence=sequence,
    )
    state.last_persisted_value = norm
    state.last_persisted_ts = observed_at
    state.policy_version = policy_version
    state.save(
        update_fields=["last_persisted_value", "last_persisted_ts", "policy_version", "quota_bucket", "quota_count"]
    )
    return "accepted"


def _lock_state(attribute_id: str) -> StoragePolicyState:
    state, _ = StoragePolicyState.objects.get_or_create(attribute_id=attribute_id)
    return StoragePolicyState.objects.select_for_update().get(pk=state.pk)


def _update_current(
    tenant_id, project_id, asset_id, attribute_id, norm, valid, value_type, observed_at, quality, source_event_id
) -> None:
    current, created = AttributeCurrent.objects.get_or_create(
        attribute_id=attribute_id,
        defaults={
            "tenant_id": tenant_id,
            "project_id": project_id,
            "asset_id": asset_id,
            "observed_at": observed_at,
            "value_type": value_type,
            "typed_value": norm if valid else None,
            "quality": quality if valid else "invalid",
            "source_event_id": source_event_id or "",
            "version": 1,
        },
    )
    if not created:
        current.tenant_id = tenant_id
        current.project_id = project_id
        current.asset_id = asset_id
        current.observed_at = observed_at
        current.value_type = value_type
        current.typed_value = norm if valid else None
        current.quality = quality if valid else "invalid"
        current.source_event_id = source_event_id or ""
        current.version = F("version") + 1
        current.save(
            update_fields=[
                "tenant_id",
                "project_id",
                "asset_id",
                "observed_at",
                "value_type",
                "typed_value",
                "quality",
                "source_event_id",
                "version",
            ]
        )


def _record_metrics(attribute_id: str, observed_at: datetime, result: IngestResult, failure: bool = False) -> None:
    bucket = observed_at.replace(minute=0, second=0, microsecond=0)
    row, _ = IngestMetrics.objects.get_or_create(attribute_id=attribute_id, window_start=bucket)
    updates = {
        "received": F("received") + result.received,
        "valid": F("valid") + result.valid,
        "invalid": F("invalid") + result.invalid,
        "duplicate": F("duplicate") + result.duplicate,
        "accepted": F("accepted") + result.accepted,
        "filtered_equal": F("filtered_equal") + result.filtered_equal,
        "filtered_quota": F("filtered_quota") + result.filtered_quota,
        "late": F("late") + result.late,
    }
    if failure:
        updates["failures"] = F("failures") + 1
    IngestMetrics.objects.filter(pk=row.pk).update(**updates)
