from __future__ import annotations

from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import AssetAttribute
from core.errors import NotFoundError
from core.permissions import TenantScopedPermission
from telemetry.serializers import IngestEventSerializer
from telemetry.services import HistoryService, StoragePolicyService
from telemetry.storage import ingest_event


def _get_attribute(attribute_id: str) -> AssetAttribute:
    try:
        return AssetAttribute.objects.select_related("asset", "tenant", "project").get(id=attribute_id)
    except AssetAttribute.DoesNotExist:
        raise NotFoundError("Attribute not found.") from None


class AttributeTelemetryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "telemetry.view"
    lookup_value_regex = "[0-9a-fA-F-]{36}"

    @action(detail=True, methods=["get"], url_path="current")
    def current(self, request, pk=None):
        attribute = _get_attribute(pk)
        self.check_object_permissions(request, attribute)
        data = HistoryService.current(pk)
        if data is None:
            return Response({"attribute_id": pk, "value": None, "quality": "unknown"}, status=200)
        return Response(data)

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, pk=None):
        attribute = _get_attribute(pk)
        self.check_object_permissions(request, attribute)
        from_ts = request.query_params.get("from")
        to_ts = request.query_params.get("to")
        rows = HistoryService.history(
            pk,
            from_ts=datetime.fromisoformat(from_ts.replace("Z", "+00:00")) if from_ts else None,
            to_ts=datetime.fromisoformat(to_ts.replace("Z", "+00:00")) if to_ts else None,
        )
        return Response(
            {
                "attribute_id": pk,
                "points": [
                    {
                        "ts": r.ts.isoformat(),
                        "value": r.typed_value,
                        "value_type": r.value_type,
                        "quality": r.quality,
                        "policy_version": r.policy_version,
                        "source_event_id": r.source_event_id,
                    }
                    for r in rows
                ],
            }
        )

    @action(detail=True, methods=["get"], url_path="stats")
    def stats(self, request, pk=None):
        attribute = _get_attribute(pk)
        self.check_object_permissions(request, attribute)
        return Response(HistoryService.stats(pk))

    @action(detail=True, methods=["get"], url_path="policy/effective")
    def policy_effective(self, request, pk=None):
        attribute = _get_attribute(pk)
        self.check_object_permissions(request, attribute)
        return Response(StoragePolicyService.effective(attribute))


class IngestView(APIView):
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "telemetry.ingest"

    def post(self, request):
        serializer = IngestEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = ingest_event(
            tenant_id=str(data["tenant_id"]),
            project_id=str(data["project_id"]) if data.get("project_id") else None,
            asset_id=str(data["asset_id"]),
            attribute_id=str(data["attribute_id"]),
            value=data["value"],
            value_type=data["value_type"],
            observed_at=data["observed_at"],
            quality=data.get("quality", "good"),
            source_event_id=data.get("source_event_id", ""),
            sequence=data.get("sequence"),
            transport=data.get("transport", "mqtt"),
            topic=data.get("topic", ""),
        )
        return Response(result.as_dict(), status=status.HTTP_200_OK)
