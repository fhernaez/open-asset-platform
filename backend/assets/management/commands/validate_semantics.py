"""Validate the semantic projection with SHACL (rules from manifests)."""
from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Validate assets with SHACL shapes generated from manifest rules."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", dest="tenant_slug", default=None)

    def handle(self, *args, **options):
        from assets.semantics import validate_with_shacl
        from platforms.models import Tenant

        tenant = None
        if options.get("tenant_slug"):
            tenant = Tenant.objects.get(slug=options["tenant_slug"])
        code, issues = validate_with_shacl(tenant=tenant)
        for issue in issues:
            self.stderr.write(issue)
        if code == 0:
            self.stdout.write(self.style.SUCCESS("SHACL validation: conforms."))
        else:
            self.stderr.write(f"SHACL validation: {len(issues)} violation(s).")
            raise SystemExit(1)
