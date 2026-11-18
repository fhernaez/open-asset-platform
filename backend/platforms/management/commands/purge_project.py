"""Purge everything linked to a project, in dependency order (no cascades).

Usage:
    manage.py purge_project --code <project_code>            # dry-run (counts)
    manage.py purge_project --code <project_code> --yes      # really delete

Deletion order (children first):
    spatial.ScenePlacement -> connectivity.GatewayBinding -> connectivity.Gateway
    -> telemetry (points/current/metrics/policy states) -> assets.AssetAttribute
    -> assets.Asset -> dashboards.Widget/Dashboard -> spatial.SceneLayer/Scene
    -> platforms.AuditLog(project) -> platforms.Project
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Purge all data linked to a project (dependency-ordered)."

    def add_arguments(self, parser):
        parser.add_argument("--code", dest="code", required=True)
        parser.add_argument("--yes", action="store_true", dest="yes")

    def handle(self, *args, **options):
        from platforms.models import Project

        try:
            project = Project.objects.select_related("tenant").get(code=options["code"])
        except Project.DoesNotExist:
            self.stderr.write(f"project with code '{options['code']}' not found.")
            raise SystemExit(1) from None

        counts = self._counts(project)
        total = sum(counts.values())
        self.stdout.write(f"project={project.code} tenant={project.tenant.slug}")
        for name, count in counts.items():
            self.stdout.write(f"  {name}: {count}")
        if not options["yes"]:
            self.stdout.write("DRY RUN: re-run with --yes to delete.")
            return

        with transaction.atomic():
            self._delete(project)
        self.stdout.write(self.style.SUCCESS(f"purge_project: deleted {total} rows for '{project.code}'."))

    def _asset_ids(self, project):
        from assets.models import Asset

        return list(Asset.objects.filter(project=project).values_list("id", flat=True))

    def _attribute_ids(self, asset_ids):
        from assets.models import AssetAttribute

        return list(AssetAttribute.objects.filter(asset_id__in=asset_ids).values_list("id", flat=True))

    def _counts(self, project) -> dict:
        from connectivity.models import Gateway, GatewayBinding
        from dashboards.models import Dashboard, Widget
        from platforms.models import AuditLog
        from spatial.models import Scene, SceneLayer, ScenePlacement
        from telemetry.models import AttributeCurrent, IngestMetrics, StoragePolicyState, TelemetryPoint

        asset_ids = self._asset_ids(project)
        attribute_ids = self._attribute_ids(asset_ids)
        return {
            "scene_placements": ScenePlacement.objects.filter(asset_id__in=asset_ids).count(),
            "bindings": GatewayBinding.objects.filter(asset_id__in=asset_ids).count(),
            "gateways": Gateway.objects.filter(asset_id__in=asset_ids).count(),
            "telemetry_points": TelemetryPoint.objects.filter(attribute_id__in=attribute_ids).count(),
            "currents": AttributeCurrent.objects.filter(attribute_id__in=attribute_ids).count(),
            "metrics": IngestMetrics.objects.filter(attribute_id__in=attribute_ids).count(),
            "policy_states": StoragePolicyState.objects.filter(attribute_id__in=attribute_ids).count(),
            "attributes": len(attribute_ids),
            "assets": len(asset_ids),
            "widgets": Widget.objects.filter(dashboard__project=project).count(),
            "dashboards": Dashboard.objects.filter(project=project).count(),
            "scene_layers": SceneLayer.objects.filter(scene__project=project).count(),
            "scenes": Scene.objects.filter(project=project).count(),
            "audit_logs": AuditLog.objects.filter(project=project).count(),
        }

    def _delete(self, project) -> None:
        from assets.models import Asset, AssetAttribute
        from connectivity.models import Gateway, GatewayBinding
        from dashboards.models import Dashboard, Widget
        from platforms.models import AuditLog
        from spatial.models import Scene, SceneLayer, ScenePlacement
        from telemetry.models import AttributeCurrent, IngestMetrics, StoragePolicyState, TelemetryPoint

        asset_ids = self._asset_ids(project)
        attribute_ids = self._attribute_ids(asset_ids)

        ScenePlacement.objects.filter(asset_id__in=asset_ids).delete()
        GatewayBinding.objects.filter(asset_id__in=asset_ids).delete()
        Gateway.objects.filter(asset_id__in=asset_ids).delete()
        TelemetryPoint.objects.filter(attribute_id__in=attribute_ids).delete()
        AttributeCurrent.objects.filter(attribute_id__in=attribute_ids).delete()
        IngestMetrics.objects.filter(attribute_id__in=attribute_ids).delete()
        StoragePolicyState.objects.filter(attribute_id__in=attribute_ids).delete()
        AssetAttribute.objects.filter(asset_id__in=asset_ids).delete()
        Asset.objects.filter(project=project).delete()
        Widget.objects.filter(dashboard__project=project).delete()
        Dashboard.objects.filter(project=project).delete()
        SceneLayer.objects.filter(scene__project=project).delete()
        Scene.objects.filter(project=project).delete()
        AuditLog.objects.filter(project=project).delete()
        project.delete()
