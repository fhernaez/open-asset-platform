from __future__ import annotations

import hashlib
import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import TenantScopedPermission
from core.viewsets import TenantScopedViewSet
from mqtt.models import (
    BrokerConnection,
    MqttAgent,
    MqttBinding,
    MqttDiscoveryTemplate,
    MqttSubscriptionHealth,
)
from mqtt.serializers import (
    BrokerConnectionSerializer,
    IngestMessageSerializer,
    MqttAgentSerializer,
    MqttBindingSerializer,
    MqttDiscoveryTemplateSerializer,
    MqttSubscriptionHealthSerializer,
    StoragePolicySerializer,
)
from mqtt.services import process_message


class BrokerConnectionViewSet(TenantScopedViewSet):
    serializer_class = BrokerConnectionSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "mqtt.manage"
    tenant_field = "tenant_id"
    queryset = BrokerConnection.objects.all()


class MqttAgentViewSet(TenantScopedViewSet):
    serializer_class = MqttAgentSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "mqtt.manage"
    tenant_field = "tenant_id"
    queryset = MqttAgent.objects.select_related("broker").all()

    @action(detail=True, methods=["get"], url_path="storage-policy")
    def get_storage_policy(self, request, pk=None):
        agent = self.get_object()
        defaults = agent.storage_policy_defaults or {}
        version = hashlib.sha256(json.dumps(defaults, sort_keys=True).encode()).hexdigest()[:16]
        return Response({"agent_id": str(agent.id), "storage_policy": defaults, "policy_version": version})

    @action(detail=True, methods=["put"], url_path="storage-policy")
    def put_storage_policy(self, request, pk=None):
        agent = self.get_object()
        serializer = StoragePolicySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        defaults = dict(agent.storage_policy_defaults or {})
        data = dict(serializer.validated_data)
        data.pop("storageDatapoint", None)
        defaults.update({k: v for k, v in data.items() if v is not None})
        agent.storage_policy_defaults = defaults
        agent.save(update_fields=["storage_policy_defaults"])
        version = hashlib.sha256(json.dumps(defaults, sort_keys=True).encode()).hexdigest()[:16]
        return Response({"agent_id": str(agent.id), "storage_policy": defaults, "policy_version": version})

    @action(detail=True, methods=["post"], url_path="ingest")
    def ingest(self, request, pk=None):
        agent = self.get_object()
        serializer = IngestMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = process_message(
            str(agent.id),
            serializer.validated_data["topic"],
            serializer.validated_data["payload"],
            source_event_id=serializer.validated_data.get("source_event_id", ""),
        )
        return Response({"matched": len(results), "results": results})

    @action(detail=True, methods=["get"], url_path="test-connection")
    def test_connection(self, request, pk=None):
        agent = self.get_object()
        return Response({"agent_id": str(agent.id), "status": agent.connection_status})


class MqttBindingViewSet(TenantScopedViewSet):
    serializer_class = MqttBindingSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "mqtt.manage"
    tenant_field = "tenant_id"
    queryset = MqttBinding.objects.select_related("agent", "asset", "attribute").all()

    def get_queryset(self):
        qs = super().get_queryset()
        agent_id = self.request.query_params.get("agent")
        if agent_id:
            qs = qs.filter(agent_id=agent_id)
        return qs


class MqttDiscoveryTemplateViewSet(TenantScopedViewSet):
    serializer_class = MqttDiscoveryTemplateSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "mqtt.manage"
    tenant_field = "tenant_id"
    queryset = MqttDiscoveryTemplate.objects.all()


class MqttSubscriptionHealthViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MqttSubscriptionHealthSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "mqtt.view"
    queryset = MqttSubscriptionHealth.objects.select_related("agent").all()
