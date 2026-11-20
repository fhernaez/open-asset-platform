"""Export the semantic projection as RDF (Brick/Haystack/81346)."""
from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export the RDF projection of assets (turtle)."

    def add_arguments(self, parser):
        parser.add_argument("--tenant", dest="tenant_slug", default=None)
        parser.add_argument("--file", dest="file", default=None)

    def handle(self, *args, **options):
        from assets.semantics import build_graph
        from platforms.models import Tenant

        tenant = None
        if options.get("tenant_slug"):
            tenant = Tenant.objects.get(slug=options["tenant_slug"])
        turtle = build_graph(tenant=tenant)
        if options.get("file"):
            with open(options["file"], "w", encoding="utf-8") as handle:
                handle.write(turtle)
            self.stdout.write(f"RDF written to {options['file']}")
        else:
            self.stdout.write(turtle)
