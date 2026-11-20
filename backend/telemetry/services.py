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

    # Trend (widget trend multi-serie, ADR-019) -------------------------------
    @staticmethod
    def trend(
        attribute_ids: list[str],
        *,
        from_ts=None,
        to_ts=None,
        interval_seconds: int | None = None,
        downsample: str = "none",
        max_points: int = 2000,
    ) -> list[dict]:
        """Multi-attribute series with optional bucket downsampling and gap flags."""
        series: list[dict] = []
        for attribute_id in attribute_ids:
            rows = HistoryService.history(attribute_id, from_ts=from_ts, to_ts=to_ts, limit=20000)
            points = [
                {"ts": r.ts, "value": r.typed_value, "quality": r.quality}
                for r in rows
                if r.typed_value is not None
            ]
            if downsample == "avg" and interval_seconds:
                points = _bucket_average(points, interval_seconds)
            elif downsample == "lttb" and len(points) > max_points:
                points = _lttb(points, max_points)
            series.append(_with_gaps(points, interval_seconds))
        return series


_QUALITY_RANK = {"invalid": 0, "stale": 1, "good": 2}


def _bucket_average(points: list[dict], interval_seconds: int) -> list[dict]:
    if not points:
        return []
    buckets: dict[int, dict] = {}
    for point in points:
        key = int(point["ts"].timestamp() // interval_seconds)
        bucket = buckets.get(key)
        if bucket is None:
            bucket = {"ts": point["ts"], "sum": 0.0, "count": 0, "quality": point["quality"]}
            buckets[key] = bucket
        try:
            bucket["sum"] += float(point["value"])
            bucket["count"] += 1
        except (TypeError, ValueError):
            continue
        if _QUALITY_RANK.get(point["quality"], 2) < _QUALITY_RANK.get(bucket["quality"], 2):
            bucket["quality"] = point["quality"]
    result = []
    for key in sorted(buckets):
        bucket = buckets[key]
        result.append({"ts": bucket["ts"], "value": bucket["sum"] / bucket["count"], "quality": bucket["quality"]})
    return result


def _lttb(points: list[dict], max_points: int) -> list[dict]:
    """Largest-Triangle-Three-Buckets downsampling preserving visual shape."""
    if len(points) <= max_points or max_points < 3:
        return points
    bucket_size = (len(points) - 2) / (max_points - 2)
    sampled: list[dict] = [points[0]]
    for i in range(max_points - 2):
        start = int((i + 1) * bucket_size) + 1
        end = int((i + 2) * bucket_size) + 1
        end = min(end, len(points) - 1)
        avg = {"ts": points[0]["ts"], "sum": 0.0, "count": 0}
        for j in range(start, end):
            avg["sum"] += float(points[j]["value"])
            avg["count"] += 1
        if avg["count"] == 0:
            if start >= len(points):
                break
            sampled.append(points[start])
            continue
        previous = sampled[-1]
        next_point = points[end]
        max_area = -1.0
        chosen = points[start]
        for j in range(start, end):
            area = abs(
                (float(previous["ts"].timestamp()) - float(next_point["ts"].timestamp()))
                * (float(points[j]["value"]) - float(previous["value"]))
                - (float(previous["ts"].timestamp()) - float(points[j]["ts"].timestamp()))
                * (float(next_point["value"]) - float(previous["value"]))
            )
            if area > max_area:
                max_area = area
                chosen = points[j]
        sampled.append(chosen)
    sampled.append(points[-1])
    return sampled


def _with_gaps(points: list[dict], interval_seconds: int | None) -> list[dict]:
    threshold = (interval_seconds or 60) * 2.5
    result = []
    previous_ts = None
    for point in points:
        gap = previous_ts is not None and (point["ts"] - previous_ts).total_seconds() > threshold
        result.append({"ts": point["ts"], "value": point["value"], "quality": point["quality"], "gap": gap})
        previous_ts = point["ts"]
    return result


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
            "source": (
                "agent+attribute"
                if (agent_default and attribute.history_policy_override)
                else ("agent" if agent_default else ("attribute" if attribute.history_policy_override else "default"))
            ),
            "mode": policy.get("mode"),
            "max_samples": {"count": max_samples.get("count"), "window": max_samples.get("window")},
            "window_strategy": max_samples.get("strategy"),
            "compare": policy.get("compare"),
            "policy_version": policy_version,
        }
