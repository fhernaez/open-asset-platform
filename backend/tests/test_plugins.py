"""Plugin registry and seed-once activation tests."""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from plugins.models import PluginActivation, PluginDefinition
from plugins.services import PluginManager


@pytest.fixture
def api():
    return APIClient()


def test_sync_definitions_idempotent(db):
    first = PluginManager.sync_definitions()
    second = PluginManager.sync_definitions()
    assert first["definitions_created"] > 0
    assert second["definitions_created"] == 0
    assert PluginDefinition.objects.filter(slug="oap.mqtt").exists()


def test_seed_once_does_not_overwrite(db, monkeypatch):
    monkeypatch.setenv("PLUGIN_MQTT_DEFAULT_ENABLED", "true")
    PluginManager.sync_definitions()
    manifest = {"slug": "oap.mqtt", "env_flag": "PLUGIN_MQTT_DEFAULT_ENABLED"}
    assert PluginManager.seed_activation(manifest) is True

    # Simulate admin disabling, then re-seed: activation must stay disabled.
    PluginManager.set_enabled("oap.mqtt", False)
    activation = PluginActivation.objects.get(definition__slug="oap.mqtt")
    assert activation.enabled is False

    PluginManager.seed_activation(manifest)
    activation.refresh_from_db()
    assert activation.enabled is False


def test_core_cannot_be_disabled(db):
    PluginManager.sync_definitions()
    from core.errors import ConflictError

    with pytest.raises(ConflictError):
        PluginManager.set_enabled("oap.asset_registry", False)


def test_plugin_activation_api(api, platform_admin):
    PluginManager.sync_definitions()
    api.force_authenticate(user=platform_admin)
    response = api.get("/api/v1/plugins/")
    assert response.status_code == 200
    assert any(p["slug"] == "oap.mqtt" for p in response.data)

    patch = api.patch("/api/v1/plugins/oap.mqtt/activation/", {"enabled": False}, format="json")
    assert patch.status_code == 200, patch.data
    assert patch.data["enabled"] is False
