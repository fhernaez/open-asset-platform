from __future__ import annotations

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from connectivity.models import Gateway, GatewayBinding
from connectivity.serializers import GatewayBindingSerializer, GatewaySerializer
from connectivity.services import ensure_gateway_asset_kind, process_message, validate_gateway_config
from core.errors import ValidationError
from core.permissions import TenantScopedPermission
from core.viewsets import TenantScopedViewSet


class GatewayViewSet(TenantScopedViewSet):
    serializer_class = GatewaySerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "mqtt.manage"
    tenant_field = "tenant_id"
    queryset = Gateway.objects.select_related("asset", "asset__asset_type").all()

    def perform_create(self, serializer):
        gateway = serializer.save()
        ensure_gateway_asset_kind(gateway)
        errors = validate_gateway_config(gateway)
        if errors:
            raise ValidationError("; ".join(errors))

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        gateway = serializer.save()
        ensure_gateway_asset_kind(gateway)
        errors = validate_gateway_config(gateway)
        if errors:
            raise ValidationError("; ".join(errors))

    @action(detail=True, methods=["get"], url_path="test-connection")
    def test_connection(self, request, pk=None):
        gateway = self.get_object()
        return Response({"gateway_id": str(gateway.id), "status": gateway.connection_status})

    @action(detail=True, methods=["get", "put"], url_path="storage-policy")
    def storage_policy(self, request, pk=None):
        gateway = self.get_object()
        if request.method == "PUT":
            policy = request.data.get("storage_policy")
            if policy is not None and not isinstance(policy, dict):
                from core.errors import ValidationError

                raise ValidationError("storage_policy must be an object.")
            config = dict(gateway.config or {})
            config["storage_policy"] = policy
            gateway.config = config
            gateway.save(update_fields=["config"])
        return Response(
            {
                "gateway_id": str(gateway.id),
                "storage_policy": (gateway.config or {}).get("storage_policy"),
            }
        )

    @action(detail=True, methods=["post"], url_path="ingest")
    def ingest(self, request, pk=None):
        gateway = self.get_object()
        topic = request.data.get("topic", "")
        payload = request.data.get("payload", "")
        source_event_id = request.data.get("source_event_id", "")
        results = process_message(str(gateway.id), topic, payload, source_event_id=source_event_id)
        return Response({"matched": len(results), "results": results})


class GatewayBindingViewSet(TenantScopedViewSet):
    serializer_class = GatewayBindingSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "mqtt.manage"
    tenant_field = "tenant_id"
    queryset = GatewayBinding.objects.select_related("gateway", "asset", "attribute").all()

    def get_queryset(self):
        qs = super().get_queryset()
        gateway_id = self.request.query_params.get("gateway")
        if gateway_id:
            qs = qs.filter(gateway_id=gateway_id)
        return qs

    def perform_create(self, serializer):
        binding = serializer.save()
        # Tenant scoping follows the gateway.
        binding.tenant = binding.gateway.tenant
        binding.project = binding.gateway.project
        binding.save(update_fields=["tenant", "project"])

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        binding = serializer.save()
        binding.tenant = binding.gateway.tenant
        binding.project = binding.gateway.project
        binding.save(update_fields=["tenant", "project"])
