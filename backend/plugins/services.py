"""Plugin manager: definition sync, activation, health, dependency checks."""

from __future__ import annotations

import os

from core.errors import ConflictError, NotFoundError
from plugins.models import PluginActivation, PluginDefinition, PluginInstallation
from plugins.registry import ALL_MANIFESTS


def _env_flag(manifest: dict, default: bool = False) -> bool:
    flag = manifest.get("env_flag")
    if not flag:
        return default
    return os.environ.get(flag, "true" if default else "false").strip().lower() in {"1", "true", "yes", "on"}


def locked_slugs() -> set[str]:
    raw = os.environ.get("PLUGIN_LOCKED_DISABLED", "")
    return {s.strip() for s in raw.split(",") if s.strip()}


class PluginManager:
    @staticmethod
    def sync_definitions() -> dict:
        """Seed definitions/installations once; never overwrite activation."""
        created = 0
        installed = 0
        for manifest in ALL_MANIFESTS:
            definition, was_created = PluginDefinition.objects.get_or_create(
                slug=manifest["slug"],
                defaults={
                    "name": manifest["name"],
                    "version": manifest.get("version", "1.0.0"),
                    "core_contract": manifest.get("core_contract", ""),
                    "kind": manifest.get("kind", "django_app"),
                    "requires": manifest.get("requires", []),
                    "provides": manifest.get("provides", []),
                    "permissions": manifest.get("permissions", []),
                    "is_core": manifest.get("is_core", False),
                    "health_status": "healthy",
                },
            )
            if was_created:
                created += 1
            PluginInstallation.objects.get_or_create(definition=definition, version=definition.version)
            installed += 1
        return {"definitions_created": created, "installations": installed}

    @staticmethod
    def seed_activation(manifest: dict) -> bool:
        definition = PluginDefinition.objects.get(slug=manifest["slug"])
        activation, created = PluginActivation.objects.get_or_create(
            definition=definition,
            tenant=None,
            project=None,
            defaults={"enabled": _env_flag(manifest), "locked": False},
        )
        if not created and manifest.get("env_flag"):
            activation.locked = manifest["slug"] in locked_slugs()
            activation.save(update_fields=["locked"])
        return created

    @staticmethod
    def is_enabled(slug: str, tenant=None) -> bool:
        try:
            definition = PluginDefinition.objects.get(slug=slug)
        except PluginDefinition.DoesNotExist:
            return False
        activation = PluginActivation.objects.filter(definition=definition, tenant=tenant, project=None).first()
        if activation is None:
            return definition.is_core
        return activation.enabled

    @staticmethod
    def list_plugins(tenant=None) -> list[dict]:
        result = []
        for manifest in ALL_MANIFESTS:
            definition = PluginDefinition.objects.filter(slug=manifest["slug"]).first()
            if definition is None:
                continue
            activation = PluginActivation.objects.filter(definition=definition, tenant=tenant, project=None).first()
            enabled = activation.enabled if activation else definition.is_core
            locked = activation.locked if activation else (manifest["slug"] in locked_slugs())
            result.append(
                {
                    "slug": definition.slug,
                    "name": definition.name,
                    "version": definition.version,
                    "installed": True,
                    "enabled": enabled,
                    "effective": enabled and not locked,
                    "locked": locked,
                    "is_core": definition.is_core,
                    "health": definition.health_status,
                    "restart_required": False,
                    "dependencies": definition.requires,
                    "permissions": definition.permissions,
                }
            )
        return result

    @staticmethod
    def set_enabled(slug: str, enabled: bool, *, actor=None, tenant=None) -> dict:
        try:
            definition = PluginDefinition.objects.get(slug=slug)
        except PluginDefinition.DoesNotExist:
            raise NotFoundError(f"Plugin '{slug}' not found.") from None
        if definition.is_core and not enabled:
            raise ConflictError("Core capabilities cannot be disabled.")
        activation, _ = PluginActivation.objects.get_or_create(
            definition=definition, tenant=tenant, project=None, defaults={"enabled": False, "locked": False}
        )
        if activation.locked:
            raise ConflictError(f"Plugin '{slug}' is locked by deployment policy.")
        for req in definition.requires:
            if not PluginDefinition.objects.filter(slug=req, is_core=True).exists():
                raise ConflictError(f"Dependency '{req}' is not installed.")
        activation.enabled = enabled
        activation.save(update_fields=["enabled"])
        return {
            "slug": slug,
            "enabled": enabled,
            "effective": enabled and not activation.locked,
            "locked": activation.locked,
        }
