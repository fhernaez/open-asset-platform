"""Built-in plugin manifests (installed vs enabled).

Django apps bundled in the image are "installed" at build time; the GUI only
toggles activation, never loads code at runtime.
"""

from __future__ import annotations

PLUGIN_MANIFESTS: list[dict] = [
    {
        "slug": "oap.connectivity",
        "name": "Conectividad (gateways)",
        "version": "1.0.0",
        "core_contract": ">=1.0.0,<2.0.0",
        "kind": "django_app",
        "requires": ["oap.asset_registry", "oap.telemetry", "oap.identity"],
        "provides": ["iot.connectivity.gateway", "iot.connectivity.storage_policy"],
        "permissions": ["mqtt.view", "mqtt.manage"],
        "is_core": False,
        "env_flag": "PLUGIN_CONNECTIVITY_DEFAULT_ENABLED",
    },
]

CORE_CAPABILITIES: list[dict] = [
    {"slug": "oap.platform", "name": "Platform", "is_core": True, "version": "1.0.0"},
    {"slug": "oap.identity", "name": "Identity", "is_core": True, "version": "1.0.0"},
    {"slug": "oap.asset_registry", "name": "Asset registry", "is_core": True, "version": "1.0.0"},
    {"slug": "oap.telemetry", "name": "Telemetry", "is_core": True, "version": "1.0.0"},
    {"slug": "oap.events", "name": "Events", "is_core": True, "version": "1.0.0"},
]

ALL_MANIFESTS = CORE_CAPABILITIES + PLUGIN_MANIFESTS
