"""Validación de manifiestos ASSET_TYPE_SCHEMA v1."""

from __future__ import annotations

ALLOWED_VALUE_TYPES = {"string", "boolean", "number", "json"}
ALLOWED_KINDS = {"standard", "gateway"}
ALLOWED_CONN_TYPES = {"string", "int", "bool", "secret", "select"}


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    code = manifest.get("code")
    if not code or not str(code).strip():
        errors.append("code is required.")
    kind = manifest.get("kind", "standard")
    if kind not in ALLOWED_KINDS:
        errors.append(f"kind must be one of {sorted(ALLOWED_KINDS)}.")
    labels = manifest.get("label_i18n")
    if not isinstance(labels, dict) or not labels.get("es"):
        errors.append("label_i18n.es is required.")
    attributes = manifest.get("attributes", [])
    if not isinstance(attributes, list):
        errors.append("attributes must be a list.")
        return errors
    seen_codes: set[str] = set()
    for item in attributes:
        if not isinstance(item, dict):
            errors.append("each attribute must be an object.")
            continue
        attr_code = item.get("code")
        if not attr_code:
            errors.append("each attribute needs a code.")
        elif attr_code in seen_codes:
            errors.append(f"duplicate attribute code: {attr_code}")
        else:
            seen_codes.add(attr_code)
        if item.get("value_type", "number") not in ALLOWED_VALUE_TYPES:
            errors.append(f"attribute {attr_code or '?'}: invalid value_type.")
        attr_labels = item.get("label_i18n")
        if not isinstance(attr_labels, dict) or not attr_labels.get("es"):
            errors.append(f"attribute {attr_code or '?'}: label_i18n.es is required.")
    if kind == "gateway":
        conn = manifest.get("connection_schema")
        if not isinstance(conn, list) or not conn:
            errors.append("gateway manifests need a connection_schema list.")
        else:
            seen_fields: set[str] = set()
            for field in conn:
                if not isinstance(field, dict):
                    errors.append("each connection field must be an object.")
                    continue
                name = field.get("field")
                if not name:
                    errors.append("connection field needs 'field'.")
                elif name in seen_fields:
                    errors.append(f"duplicate connection field: {name}")
                else:
                    seen_fields.add(name)
                if field.get("type") not in ALLOWED_CONN_TYPES:
                    errors.append(f"connection field {name or '?'}: invalid type.")
                field_labels = field.get("label_i18n")
                if not isinstance(field_labels, dict) or not field_labels.get("es"):
                    errors.append(f"connection field {name or '?'}: label_i18n.es is required.")
    return errors
