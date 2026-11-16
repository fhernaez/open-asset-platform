"""Seed-once bootstrap: system roles and the initial platform administrator.

Runs as part of the ``migrate`` one-shot service with ``--seed-missing-only``.
It never overwrites existing roles, users, or administrable settings.
"""

from __future__ import annotations

import os
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

SYSTEM_ROLES = {
    "tenant_admin": {
        "name": "Tenant administrator",
        "description": "Full control within a tenant.",
        "permissions": ["*"],
    },
    "operator": {
        "name": "Operator",
        "description": "Manage assets, telemetry and rules within a tenant.",
        "permissions": [
            "assets.view",
            "assets.manage",
            "telemetry.view",
            "telemetry.policy.write",
            "mqtt.view",
            "mqtt.manage",
            "rules.manage",
        ],
    },
    "viewer": {
        "name": "Viewer",
        "description": "Read-only access to assets and telemetry.",
        "permissions": ["assets.view", "telemetry.view", "mqtt.view", "plugins.view"],
    },
    "technician": {
        "name": "Technician",
        "description": "Field technician with CMMS access.",
        "permissions": ["assets.view", "telemetry.view", "cmms.view", "cmms.manage"],
    },
}


class Command(BaseCommand):
    help = "Seed system roles and the initial admin (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--seed-missing-only", action="store_true", dest="seed_missing_only")

    def handle(self, *args, **options):
        from core.models import Role

        created_roles = 0
        for slug, spec in SYSTEM_ROLES.items():
            _, created = Role.objects.get_or_create(slug=slug, defaults=spec)
            if created:
                created_roles += 1

        admin_created = self._seed_admin()
        plugins_result = self._seed_plugins()
        self.stdout.write(
            self.style.SUCCESS(
                f"bootstrap_config: roles_seeded={created_roles} admin_created={admin_created} plugins={plugins_result}"
            )
        )

    def _seed_admin(self) -> bool:
        email = os.environ.get("AUTH_BOOTSTRAP_ADMIN_EMAIL", "")
        password_file = os.environ.get("AUTH_BOOTSTRAP_ADMIN_PASSWORD_FILE", "")
        if not email:
            return False
        password = ""
        if password_file and Path(password_file).exists():
            password = Path(password_file).read_text(encoding="utf-8").strip()
        if not password:
            return False
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            email=email.lower(),
            defaults={"is_staff": True, "is_platform_admin": True, "is_superuser": True},
        )
        if created:
            user.set_password(password)
            user.save(update_fields=["password"])
        return created

    def _seed_plugins(self) -> dict:
        from plugins.registry import PLUGIN_MANIFESTS
        from plugins.services import PluginManager

        PluginManager.sync_definitions()
        activations = 0
        for manifest in PLUGIN_MANIFESTS:
            if PluginManager.seed_activation(manifest):
                activations += 1
        return {"new_activations": activations}
