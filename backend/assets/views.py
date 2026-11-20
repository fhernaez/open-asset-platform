from __future__ import annotations

import logging

from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from assets.models import Asset, AssetAttribute, AssetType, Unit
from assets.serializers import (
    AssetAttributeSerializer,
    AssetSerializer,
    AssetTypeSerializer,
    UnitSerializer,
)
from core.errors import ConflictError, ValidationError
from core.permissions import TenantScopedPermission
from core.utils import strip_control_chars
from core.viewsets import TenantScopedViewSet
from platforms.services import AuditService, require_membership

logger = logging.getLogger(__name__)


class UnitViewSet(TenantScopedViewSet):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    queryset = Unit.objects.all()
    unscoped = True


class AssetTypeViewSet(TenantScopedViewSet):
    serializer_class = AssetTypeSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.manage"
    tenant_field = "tenant_id"
    queryset = AssetType.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        tenant_id = self.request.query_params.get("tenant")
        kind = self.request.query_params.get("kind")
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        if kind:
            qs = qs.filter(kind=kind)
        return qs

    def perform_create(self, serializer):
        obj = serializer.save(tenant=self._tenant_for_request())
        AuditService.record(
            actor=self.request.user,
            action="assettype.create",
            resource_type="assettype",
            resource_id=str(obj.id),
            tenant=obj.tenant,
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        if "schema" in serializer.validated_data:
            schema = dict(serializer.validated_data.get("schema") or {})
            schema["custom"] = True
            serializer.validated_data["schema"] = schema
        obj = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="assettype.update",
            resource_type="assettype",
            resource_id=str(obj.id),
            tenant=obj.tenant,
        )

    def perform_destroy(self, instance):
        count = Asset.objects.filter(asset_type=instance).count()
        if count:
            raise ConflictError(f"Tipología en uso por {count} activos; reasigná o eliminá esos activos primero.")
        tenant = instance.tenant
        instance.delete()
        AuditService.record(
            actor=self.request.user,
            action="assettype.delete",
            resource_type="assettype",
            resource_id=str(instance.id),
            tenant=tenant,
        )

    def _tenant_for_request(self):
        from platforms.models import Membership, Tenant

        tenant = self.request.data.get("tenant")
        if tenant:
            return Tenant.objects.get(id=tenant)
        membership = Membership.objects.filter(user=self.request.user, is_active=True).first()
        return membership.tenant if membership else None


class AssetViewSet(TenantScopedViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.manage"
    tenant_field = "tenant_id"
    queryset = Asset.objects.select_related("asset_type", "parent").all()

    def get_queryset(self):
        qs = super().get_queryset()
        tenant_id = self.request.query_params.get("tenant")
        project_id = self.request.query_params.get("project")
        kind = self.request.query_params.get("kind")
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        if project_id:
            qs = qs.filter(project_id=project_id)
        if kind in {"standard", "gateway"}:
            qs = qs.filter(asset_type__kind=kind)
        elif kind == "non_gateway":
            qs = qs.exclude(asset_type__kind="gateway")
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gateway = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = dict(serializer.data)
        if gateway is not None:
            data["gateway_id"] = str(gateway.id)
        from rest_framework.response import Response

        return Response(data, status=201, headers=headers)

    def perform_create(self, serializer):
        from assets.services import apply_type_template
        from connectivity.models import Gateway, GatewayBinding
        from connectivity.services import validate_gateway_config

        tenant = self._resolve_tenant(serializer.validated_data)
        require_membership(self.request.user, tenant, "assets.manage")
        project = serializer.validated_data.get("project")
        if project is not None and project.tenant_id != tenant.id:
            raise ValidationError("project must belong to the asset tenant.")

        with transaction.atomic():
            asset = serializer.save(tenant=tenant)
            apply_type_template(asset)
            from assets.services import validate_manifest_rules

            rule_errors = validate_manifest_rules(asset)
            if rule_errors:
                raise ValidationError("; ".join(rule_errors))
            gateway = None
            asset_type = asset.asset_type
            if asset_type is not None and asset_type.kind == "gateway":
                raw_config = self.request.data.get("gateway_config") or {}
                config = dict(raw_config) if isinstance(raw_config, dict) else {}
                config = strip_control_chars(config)
                code = asset_type.code
                if code == "gateway":
                    protocol = config.get("protocol") or "mqtt"
                else:
                    config.pop("protocol", None)
                    protocol = code.removeprefix("gateway-") if code.startswith("gateway-") else "mqtt"
                try:
                    gateway = Gateway.objects.create(
                        tenant=tenant,
                        project=project,
                        asset=asset,
                        protocol=protocol,
                        config=config,
                    )
                    errors = validate_gateway_config(gateway)
                    if errors:
                        raise ValidationError("; ".join(errors))
                except ValidationError:
                    raise
                except Exception:
                    # Fail closed with a visible log; the transaction rolls back.
                    logger.exception("failed to create gateway for asset %s", asset.id)
                    raise
            gateway_id = self.request.data.get("gateway_id")
            if gateway_id and gateway is None:
                try:
                    target = Gateway.objects.get(id=gateway_id, tenant_id=tenant.id)
                except Gateway.DoesNotExist:
                    raise ValidationError("gateway_id does not exist in this tenant.") from None
                GatewayBinding.objects.create(
                    tenant=tenant,
                    project=project,
                    gateway=target,
                    binding_type="device",
                    asset=asset,
                    address=str(asset.external_ref or asset.id),
                )
            AuditService.record(
                actor=self.request.user,
                action="asset.create",
                resource_type="asset",
                resource_id=str(asset.id),
                tenant=tenant,
            )
            return gateway

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        asset = serializer.save()
        from assets.services import validate_manifest_rules

        rule_errors = validate_manifest_rules(asset)
        if rule_errors:
            raise ValidationError("; ".join(rule_errors))
        AuditService.record(
            actor=self.request.user,
            action="asset.update",
            resource_type="asset",
            resource_id=str(asset.id),
            tenant=asset.tenant,
        )

    def perform_destroy(self, instance):
        from telemetry.models import AttributeCurrent, TelemetryPoint

        tenant = instance.tenant
        with transaction.atomic():
            attribute_ids = list(instance.attributes.values_list("id", flat=True))
            if attribute_ids:
                TelemetryPoint.objects.filter(attribute_id__in=attribute_ids).delete()
                AttributeCurrent.objects.filter(attribute_id__in=attribute_ids).delete()
            instance.attributes.all().delete()
            instance.delete()
        AuditService.record(
            actor=self.request.user,
            action="asset.delete",
            resource_type="asset",
            resource_id=str(instance.id),
            tenant=tenant,
        )

    @action(detail=True, methods=["get"], url_path="connectivity-status")
    def connectivity_status(self, request, pk=None):
        from connectivity.services import asset_connectivity_status

        asset = self.get_object()
        return Response(asset_connectivity_status(asset))

    @action(detail=True, methods=["post"], url_path="designation")
    def designation(self, request, pk=None):
        """Set a versioned 81346 designation for one aspect (=/-/+/%)."""
        from assets.services import set_designation

        asset = self.get_object()
        aspect = request.data.get("aspect")
        code = request.data.get("code")
        if aspect not in {"function", "product", "location", "type"}:
            raise ValidationError("aspect must be one of: function, product, location, type.")
        result = set_designation(asset, aspect, code)
        return Response(result)

    def _resolve_tenant(self, data):
        from platforms.models import Membership

        tenant = data.get("tenant")
        if tenant is not None:
            return tenant
        membership = Membership.objects.filter(user=self.request.user, is_active=True).first()
        if not membership:
            from core.errors import PermissionDeniedError

            raise PermissionDeniedError("No active tenant membership.")
        return membership.tenant


class AssetAttributeViewSet(TenantScopedViewSet):
    serializer_class = AssetAttributeSerializer
    permission_classes = [IsAuthenticated, TenantScopedPermission]
    permission_required = "assets.manage"
    tenant_field = "tenant_id"
    queryset = AssetAttribute.objects.select_related("asset", "unit").all()

    def get_queryset(self):
        qs = super().get_queryset()
        asset_id = self.request.query_params.get("asset")
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        return qs

    def perform_create(self, serializer):
        asset = serializer.validated_data.get("asset")
        if asset is None:
            from core.errors import ValidationError

            raise ValidationError("asset is required.")
        require_membership(self.request.user, asset.tenant, "assets.manage")
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        attr = serializer.save(tenant=asset.tenant, project=asset.project)
        AuditService.record(
            actor=self.request.user,
            action="attribute.create",
            resource_type="attribute",
            resource_id=str(attr.id),
            tenant=attr.tenant,
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("tenant", None)
        serializer.validated_data.pop("project", None)
        attr = serializer.save()
        AuditService.record(
            actor=self.request.user,
            action="attribute.update",
            resource_type="attribute",
            resource_id=str(attr.id),
            tenant=attr.tenant,
        )

    def perform_destroy(self, instance):
        from telemetry.models import AttributeCurrent, TelemetryPoint

        tenant = instance.tenant
        with transaction.atomic():
            TelemetryPoint.objects.filter(attribute_id=instance.id).delete()
            AttributeCurrent.objects.filter(attribute_id=instance.id).delete()
            instance.delete()
        AuditService.record(
            actor=self.request.user,
            action="attribute.delete",
            resource_type="attribute",
            resource_id=str(instance.id),
            tenant=tenant,
        )
