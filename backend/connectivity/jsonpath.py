"""Minimal JSONPath subset for MQTT binding extraction (no external dependency).

Supported syntax: ``$`` / empty (whole document), ``a.b.c`` dot access,
``a[0]`` / ``a[2].b`` list indexing and ``a['key']`` bracket keys.
"""

from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"(\[[^\]]*\]|[^.\[\]]+)")


def extract(payload, path: str):
    if not path or path in {"$", "."}:
        return payload
    current = payload
    for token in _TOKEN_RE.findall(path):
        if token == "$":
            continue
        if token.startswith("[") and token.endswith("]"):
            key = token[1:-1].strip()
            if (key.startswith("'") and key.endswith("'")) or (key.startswith('"') and key.endswith('"')):
                key = key[1:-1]
                current = current[key] if isinstance(current, dict) else None
            else:
                try:
                    idx = int(key)
                except ValueError:
                    return None
                current = current[idx] if isinstance(current, list) and 0 <= idx < len(current) else None
        else:
            if isinstance(current, dict):
                current = current.get(token)
            else:
                return None
        if current is None:
            return None
    return current
