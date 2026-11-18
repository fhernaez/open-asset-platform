"""Seed the built-in asset type catalog (seed-once per organization).

Usage: manage.py seed_asset_types [--tenant <slug>]
Without --tenant it seeds every existing organization. New organizations are
seeded automatically on creation (assets/apps.py signal).
"""

from __future__ import annotations

from django.core.management.base import BaseCommand

from assets.services import seed_catalog_for_tenant


class Command(BaseCommand):
    help = "Seed built-in asset type catalog per organization (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", dest="tenant_slug", default=None)
        parser.add_argument("--refresh", action="store_true", dest="refresh")

    def handle(self, *args, **options):
        from platforms.models import Tenant

        tenants = Tenant.objects.all()
        if options.get("tenant_slug"):
            tenants = tenants.filter(slug=options["tenant_slug"])
        total_types = 0
        for tenant in tenants:
            result = seed_catalog_for_tenant(tenant, refresh=options.get("refresh", False))
            total_types += result["types_created"]
            self.stdout.write(
                f"tenant={tenant.slug} types_created={result['types_created']} "
                f"types_updated={result['types_updated']} units_created={result['units_created']}"
            )
        self.stdout.write(self.style.SUCCESS(f"seed_asset_types: total_types_created={total_types}"))
