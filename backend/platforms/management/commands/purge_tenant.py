"""Purge an organization and all its data, in dependency order (no cascades).

Usage:
    manage.py purge_tenant --slug <tenant_slug>          # dry-run (counts)
    manage.py purge_tenant --slug <tenant_slug> --yes    # really delete
"""
from __future__ import annotations

from django.core.management.base import BaseCommand

from platforms.services import purge_tenant_data


class Command(BaseCommand):
    help = "Purge an organization and all its data (dependency-ordered)."

    def add_arguments(self, parser):
        parser.add_argument("--slug", dest="slug", required=True)
        parser.add_argument("--yes", action="store_true", dest="yes")

    def handle(self, *args, **options):
        from platforms.models import Tenant

        try:
            tenant = Tenant.objects.get(slug=options["slug"])
        except Tenant.DoesNotExist:
            self.stderr.write(f"tenant '{options['slug']}' not found.")
            raise SystemExit(1) from None

        if not options["yes"]:
            self.stdout.write(f"tenant={tenant.slug} — DRY RUN (re-run with --yes to delete).")
            return

        counts = purge_tenant_data(tenant)
        total = sum(counts.values())
        self.stdout.write(self.style.SUCCESS(f"purge_tenant: deleted {total} rows for '{tenant.slug}'."))
