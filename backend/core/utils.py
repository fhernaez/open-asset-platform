"""Shared helpers."""
from __future__ import annotations

from typing import Any


def strip_control_chars(value: Any) -> Any:
    """Recursively remove control characters (U+0000..U+001F) from strings.

    PostgreSQL jsonb rejects ``\u0000``; free-text fields pasted from other
    sources can carry invisible control chars. This keeps JSONField storage safe.
    """
    if isinstance(value, str):
        return "".join(ch for ch in value if ord(ch) >= 32)
    if isinstance(value, dict):
        return {strip_control_chars(k): strip_control_chars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [strip_control_chars(item) for item in value]
    return value
