"""Telemetry services: history and policy queries."""

from __future__ import annotations

from telemetry.models import AttributeCurrent, IngestMetrics, StoragePolicyState, TelemetryPoint
from telemetry.storage import effective_policy


class HistoryService:
    @staticmethod
    def current(attribute_id: str) -> dict:
        try:
            row = AttributeCurrent.objects.get(attribute_id=attribute_id)
        except AttributeCurrent.DoesNotExist:
            return None
        return {
            "attribute_id": str(row.attribute_id),
            "observed_at": row.observed_at,
            "value_type": row.value_type,
            "value": row.typed_value,
            "quality": row.quality,
            "source_event_id": row.source_event_id,
            "version": row.version,
        }

    @staticmethod
    def history(attribute_id: str, from_ts=None, to_ts=None, limit: int = 1000):
        qs = TelemetryPoint.objects.filter(attribute_id=attribute_id).order_by("ts")
        if from_ts is not None:
            qs = qs.filter(ts__gte=from_ts)
        if to_ts is not None:
            qs = qs.filter(ts__lte=to_ts)
        return qs[:limit]

    @staticmethod
    def stats(attribute_id: str) -> dict:
        metrics = IngestMetrics.objects.filter(attribute_id=attribute_id).order_by("window_start")
        totals = {
            "received": sum(m.received for m in metrics),
            "accepted": sum(m.accepted for m in metrics),
            "filtered_equal": sum(m.filtered_equal for m in metrics),
            "filtered_quota": sum(m.filtered_quota for m in metrics),
            "invalid": sum(m.invalid for m in metrics),
            "duplicate": sum(m.duplicate for m in metrics),
            "late": sum(m.late for m in metrics),
        }
        return {
            "attribute_id": str(attribute_id),
            "totals": totals,
            "samples": TelemetryPoint.objects.filter(attribute_id=attribute_id).count(),
        }


class StoragePolicyService:
    @staticmethod
    def effective(attribute, agent_default: dict | None = None) -> dict:
        policy = effective_policy(attribute.history_enabled, agent_default, attribute.history_policy_override)
        state = StoragePolicyState.objects.filter(attribute_id=attribute.id).first()
        policy_version = state.policy_version if state else None
        max_samples = policy.get("max_samples") or {}
        return {
            "attribute_id": str(attribute.id),
            "history_enabled": bool(attribute.history_enabled),
            "storage_datapoint": bool(attribute.storage_datapoint),
            "source": "agent+attribute"
            if (agent_default and attribute.history_policy_override)
            else ("agent" if agent_default else ("attribute" if attribute.history_policy_override else "default")),
            "mode": policy.get("mode"),
            "max_samples": {"count": max_samples.get("count"), "window": max_samples.get("window")},
            "window_strategy": max_samples.get("strategy"),
            "compare": policy.get("compare"),
            "policy_version": policy_version,
        }
