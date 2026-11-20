from __future__ import annotations

from datetime import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
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

    @extend_schema(responses={"200": OpenApiTypes.OBJECT})
    @action(detail=True, methods=["get"], url_path="current")
    def current(self, request, pk=None):
        attribute = _get_attribute(pk)
        self.check_object_permissions(request, attribute)
        data = HistoryService.current(pk)
        if data is None:
            return Response({"attribute_id": pk, "value": None, "quality": "unknown"}, status=200)
        return Response(data)

    @extend_schema(responses={"200": OpenApiTypes.OBJECT})
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

    @extend_schema(responses={"200": OpenApiTypes.OBJECT})
    @action(detail=True, methods=["get"], url_path="stats")
    def stats(self, request, pk=None):
        attribute = _get_attribute(pk)
        self.check_object_permissions(request, attribute)
        return Response(HistoryService.stats(pk))

    @extend_schema(responses={"200": OpenApiTypes.OBJECT})
    @action(detail=True, methods=["get"], url_path="policy/effective")
    def policy_effective(self, request, pk=None):
        attribute = _get_attribute(pk)
        self.check_object_permissions(request, attribute)
        agent_default = None
        gateway_id = request.query_params.get("gateway")
        if gateway_id:
            from connectivity.models import Gateway

            gateway = Gateway.objects.filter(id=gateway_id, tenant_id=attribute.tenant_id).first()
            if gateway is not None:
                agent_default = (gateway.config or {}).get("storage_policy")
        return Response(StoragePolicyService.effective(attribute, agent_default))


class IngestView(APIView):
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "telemetry.ingest"

    @extend_schema(request=IngestEventSerializer, responses={"200": OpenApiTypes.OBJECT})
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


def _parse_interval(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        pass
    multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    unit = value[-1]
    try:
        return int(float(value[:-1]) * multiplier[unit])
    except (KeyError, ValueError):
        return None


class TrendView(APIView):
    """Multi-attribute trend for the trend widget (ADR-019): POST attributes+range."""

    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "telemetry.view"

    @extend_schema(request=OpenApiTypes.OBJECT, responses={"200": OpenApiTypes.OBJECT})
    def post(self, request):
        from assets.models import AssetAttribute
        from core.errors import NotFoundError

        attribute_ids = request.data.get("attributes") or []
        if not isinstance(attribute_ids, list) or not attribute_ids:
            return Response({"detail": "attributes (list) is required."}, status=400)
        interval_seconds = _parse_interval(request.data.get("interval"))
        downsample = request.data.get("downsample") or "none"
        max_points = int(request.data.get("max_points") or 2000)
        from_ts = request.data.get("from")
        to_ts = request.data.get("to")

        tenant_id = request.data.get("tenant")
        if tenant_id:
            from core.errors import PermissionDeniedError
            from platforms.models import Membership
            from platforms.services import require_membership

            is_admin = request.user.is_superuser or getattr(request.user, "is_platform_admin", False)
            membership = Membership.objects.filter(user=request.user, tenant_id=tenant_id, is_active=True).first()
            if not is_admin and membership is None:
                raise PermissionDeniedError("No active membership for the requested tenant.")
            require_membership(request.user, membership.tenant if membership else None, "telemetry.view")
        else:
            from platforms.models import Membership

            membership = Membership.objects.filter(user=request.user, is_active=True).first()
            tenant_id = membership.tenant_id if membership else None
        attributes = AssetAttribute.objects.select_related("unit").filter(
            id__in=attribute_ids, tenant_id=tenant_id
        )
        by_id = {str(a.id): a for a in attributes}
        if len(by_id) != len(set(str(i) for i in attribute_ids)):
            missing = [str(i) for i in attribute_ids if str(i) not in by_id]
            raise NotFoundError(f"Attributes not found for tenant: {', '.join(missing[:5])}.")

        series = HistoryService.trend(
            [str(a.id) for a in attributes],
            from_ts=datetime.fromisoformat(from_ts.replace("Z", "+00:00")) if from_ts else None,
            to_ts=datetime.fromisoformat(to_ts.replace("Z", "+00:00")) if to_ts else None,
            interval_seconds=interval_seconds,
            downsample=downsample,
            max_points=max_points,
        )
        payload = []
        for attribute, points in zip(attributes, series, strict=True):
            unit = attribute.unit.symbol if attribute.unit is not None else None
            payload.append(
                {
                    "attribute_id": str(attribute.id),
                    "code": attribute.code,
                    "name": attribute.name,
                    "unit": unit,
                    "points": [
                        {"ts": p["ts"].isoformat(), "value": p["value"], "quality": p["quality"], "gap": p["gap"]}
                        for p in points
                    ],
                }
            )
        return Response({"interval": request.data.get("interval"), "downsample": downsample, "series": payload})
