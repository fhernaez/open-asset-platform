"""Storage policy evaluation: effective policy, on_change compare, window quota."""

from __future__ import annotations

import json
import math
import re
from datetime import UTC, datetime
from typing import Any

ALLOWED_MODES = {"all", "on_change", "min_interval", "fixed_n_per_window", "aggregate_window"}

_DURATION_RE = re.compile(
    r"^P(?!$)(?:(?P<days>\d+)D)?(?:T(?=\d)(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?$"
)
_SIMPLE_DURATION_RE = re.compile(r"^(?P<value>\d+)(?P<unit>s|m|h|d)$")


def parse_window(duration: str | int | float) -> int:
    """Parse an ISO-8601 duration or a simple ``30s/5m/1h/2d`` string to seconds."""
    if isinstance(duration, int | float):
        return int(duration)
    text = str(duration).strip()
    match = _DURATION_RE.match(text)
    if match:
        parts = match.groupdict()
        total = 0
        total += int(parts.get("days") or 0) * 86400
        total += int(parts.get("hours") or 0) * 3600
        total += int(parts.get("minutes") or 0) * 60
        total += int(parts.get("seconds") or 0)
        if total <= 0:
            raise ValueError(f"invalid duration: {duration!r}")
        return total
    simple = _SIMPLE_DURATION_RE.match(text)
    if simple:
        value = int(simple.group("value"))
        unit = simple.group("unit")
        factor = {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
        return value * factor
    raise ValueError(f"invalid duration: {duration!r}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def normalize_value(value: Any, value_type: str) -> tuple[Any | None, bool, str]:
    """Return (normalized_value, is_valid, canonical). Invalid -> (None, False, '')."""
    try:
        if value_type == "number":
            if isinstance(value, bool):
                return None, False, ""
            num = float(value)
            if not math.isfinite(num):
                return None, False, ""
            return num, True, repr(num)
        if value_type == "boolean":
            if isinstance(value, str):
                lowered = value.strip().lower()
                if lowered in {"true", "1"}:
                    return True, True, "true"
                if lowered in {"false", "0"}:
                    return False, True, "false"
                return None, False, ""
            if isinstance(value, bool):
                return value, True, "true" if value else "false"
            return None, False, ""
        if value_type == "string":
            if not isinstance(value, str):
                return None, False, ""
            return value, True, value
        if value_type == "json":
            if isinstance(value, str):
                value = json.loads(value)
            canonical = canonical_json(value)
            return value, True, canonical
        return None, False, ""
    except (ValueError, TypeError, json.JSONDecodeError):
        return None, False, ""


def is_change(new: Any, baseline: Any, value_type: str, compare: dict) -> bool:
    """True when a normalized value differs from the persisted baseline."""
    if baseline is None:
        return True
    if value_type in {"boolean", "string"}:
        return bool(new) != bool(baseline)
    if value_type == "number":
        try:
            new_num = float(new)
            base_num = float(baseline)
        except (TypeError, ValueError):
            return True
        epsilon_abs = float(compare.get("absolute_epsilon") or 0)
        epsilon_rel = compare.get("relative_epsilon")
        diff = abs(new_num - base_num)
        if diff > epsilon_abs:
            return True
        if epsilon_rel is not None:
            threshold = float(epsilon_rel) * abs(base_num)
            if diff > threshold:
                return True
        return False
    if value_type == "json":
        return canonical_json(new) != canonical_json(baseline)
    return True


def window_bucket(ts: datetime, window_seconds: int) -> int:
    epoch = int(ts.timestamp())
    return (epoch // window_seconds) * window_seconds


def merge_policy(base: dict, override: dict | None) -> dict:
    """Deep-merge an attribute override over an agent default."""
    merged = dict(base or {})
    if not override:
        return merged
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


def utcnow() -> datetime:
    return datetime.now(UTC)
