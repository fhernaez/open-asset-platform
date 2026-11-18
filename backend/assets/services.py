"""Asset services exposed to plugins (public contract)."""

from __future__ import annotations

from core.authz import AuthzService
from core.errors import NotFoundError, PermissionDeniedError


class AssetService:
    @staticmethod
    def get(asset_id, ctx):
        from assets.models import Asset

        try:
            asset = Asset.objects.select_related("tenant", "project", "asset_type").get(id=asset_id)
        except Asset.DoesNotExist:
            raise NotFoundError("Asset not found.") from None
        if not AuthzService.check(ctx.actor, "assets.view", tenant=asset.tenant, project=asset.project):
            raise PermissionDeniedError("assets.view required.")
        return asset

    @staticmethod
    def list(ctx, *, tenant_id=None, project_id=None):
        from assets.models import Asset

        qs = Asset.objects.all()
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs


class AttributeService:
    @staticmethod
    def get(attribute_id, ctx):
        from assets.models import AssetAttribute

        try:
            attr = AssetAttribute.objects.select_related("asset", "tenant", "project").get(id=attribute_id)
        except AssetAttribute.DoesNotExist:
            raise NotFoundError("Attribute not found.") from None
        if not AuthzService.check(ctx.actor, "assets.view", tenant=attr.tenant, project=attr.project):
            raise PermissionDeniedError("assets.view required.")
        return attr


def apply_type_template(asset) -> list:
    """Create attributes declared in the asset type schema (idempotent per code)."""
    from assets.models import AssetAttribute

    asset_type = asset.asset_type
    if asset_type is None:
        return []
    templates = (asset_type.schema or {}).get("attributes", [])
    created = []
    for template in templates:
        if not isinstance(template, dict) or not template.get("code"):
            continue
        code = str(template["code"])[:120]
        if AssetAttribute.objects.filter(asset=asset, code=code).exists():
            continue
        created.append(
            AssetAttribute.objects.create(
                tenant=asset.tenant,
                project=asset.project,
                asset=asset,
                name=str(template.get("name") or code)[:160],
                code=code,
                value_type=template.get("value_type", "number"),
                unit=template.get("unit"),
                storage_datapoint=bool(template.get("storage_datapoint", False)),
                history_enabled=bool(template.get("storage_datapoint", False)),
                description=str(template.get("description", ""))[:500],
                metadata=template.get("metadata") or {},
            )
        )
    return created


def seed_catalog_for_tenant(tenant, *, refresh: bool = False) -> dict:
    """Seed built-in asset types for a tenant (seed-once; never overwrite edits).

    With refresh=True, re-syncs types whose stored catalog_version is lower
    than the manifest version AND that were not customized (schema.custom).
    """
    from assets.models import AssetType, Unit
    from assets.types_catalog.manifests import MANIFESTS
    from assets.types_catalog.validate import validate_manifest

    created_types = 0
    updated_types = 0
    created_units = 0
    for manifest in MANIFESTS:
        errors = validate_manifest(manifest)
        if errors:
            raise ValueError(f"invalid manifest {manifest.get('code')}: {errors}")
        for attribute in manifest.get("attributes", []):
            symbol = attribute.get("unit")
            if symbol and not Unit.objects.filter(symbol=symbol).exists():
                Unit.objects.create(symbol=symbol, name=symbol, quantity="")
                created_units += 1
        schema = {
            "attributes": manifest.get("attributes", []),
            "catalog_version": manifest.get("catalog_version", 1),
        }
        if manifest.get("connection_schema"):
            schema["connection_schema"] = manifest["connection_schema"]
        labels = manifest.get("label_i18n") or {}
        descriptions = manifest.get("description_i18n") or {}
        icon = manifest.get("icon", "")
        defaults = {
            "name": str(labels.get("es") or manifest["code"])[:200],
            "kind": manifest.get("kind", "standard"),
            "description": str(descriptions.get("es", ""))[:500],
            "schema": {**schema, "icon": icon},
        }
        obj, created = AssetType.objects.get_or_create(tenant=tenant, code=manifest["code"], defaults=defaults)
        if created:
            created_types += 1
            continue
        if not refresh:
            continue
        stored = obj.schema or {}
        if stored.get("custom"):
            continue
        stored_version = int(stored.get("catalog_version") or 1)
        manifest_version = int(manifest.get("catalog_version", 1))
        if stored_version < manifest_version:
            obj.name = defaults["name"]
            obj.kind = defaults["kind"]
            obj.description = defaults["description"]
            obj.schema = defaults["schema"]
            obj.save(update_fields=["name", "kind", "description", "schema"])
            updated_types += 1
    return {"types_created": created_types, "types_updated": updated_types, "units_created": created_units}
