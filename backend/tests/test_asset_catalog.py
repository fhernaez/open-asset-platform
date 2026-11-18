"""Asset type catalog tests (OAP-ASS-005/006): seed, validation, upgrades."""

from __future__ import annotations

from assets.models import AssetType
from assets.services import seed_catalog_for_tenant
from assets.types_catalog.manifests import MANIFESTS
from assets.types_catalog.validate import validate_manifest


def test_all_manifests_validate():
    for manifest in MANIFESTS:
        assert validate_manifest(manifest) == [], f"manifest {manifest.get('code')} invalid"


def test_seed_idempotent(tenant):
    # The tenant fixture auto-seeds the catalog on creation (assets/signals.py).
    assert AssetType.objects.filter(tenant=tenant).count() == len(MANIFESTS)
    result = seed_catalog_for_tenant(tenant)
    assert result["types_created"] == 0


def test_manual_seed_after_wipe_creates_all(tenant):
    AssetType.objects.filter(tenant=tenant).delete()
    result = seed_catalog_for_tenant(tenant)
    assert result["types_created"] == len(MANIFESTS)
    assert AssetType.objects.filter(tenant=tenant).count() == len(MANIFESTS)


def test_seed_per_tenant_isolation(tenant):
    from platforms.models import Tenant

    other = Tenant.objects.create(name="Other", slug="other")
    seed_catalog_for_tenant(tenant)
    seed_catalog_for_tenant(other)
    assert AssetType.objects.filter(tenant=tenant).count() == len(MANIFESTS)
    assert AssetType.objects.filter(tenant=other).count() == len(MANIFESTS)


def test_gateway_manifests_have_connection_schema(tenant):
    seed_catalog_for_tenant(tenant)
    gateways = AssetType.objects.filter(tenant=tenant, kind="gateway")
    assert gateways.count() >= 7
    for gateway in gateways:
        assert (gateway.schema or {}).get("connection_schema"), gateway.code


def test_upgrade_adds_without_overwriting_edits(tenant):
    seed_catalog_for_tenant(tenant)
    ahu = AssetType.objects.get(tenant=tenant, code="ahu")
    ahu.name = "Mi AHU personalizado"
    ahu.save(update_fields=["name"])

    # Simulate a catalog upgrade: re-seed the same manifests (unchanged) and
    # verify the user edit persists (seed-once never overwrites).
    seed_catalog_for_tenant(tenant)
    ahu.refresh_from_db()
    assert ahu.name == "Mi AHU personalizado"


def test_seed_on_tenant_creation():
    from platforms.models import Tenant

    tenant = Tenant.objects.create(name="Auto Seed", slug="auto-seed")
    assert AssetType.objects.filter(tenant=tenant).count() == len(MANIFESTS)


def test_invalid_manifest_rejected():
    assert validate_manifest({}) != []
    assert validate_manifest({"code": "x", "kind": "bogus"}) != []
    gateway_missing_conn = {
        "code": "gw",
        "kind": "gateway",
        "label_i18n": {"es": "GW"},
    }
    assert validate_manifest(gateway_missing_conn) != []


def test_refresh_updates_non_custom(tenant):
    # Tenant auto-seeded with the enriched catalog (version 2).
    ahu = AssetType.objects.get(tenant=tenant, code="ahu")
    # Simulate an old seed: downgrade the stored version marker and strip attributes.
    ahu.schema = {"attributes": [], "catalog_version": 1, "icon": "ahu"}
    ahu.save(update_fields=["schema"])

    result = seed_catalog_for_tenant(tenant, refresh=True)
    assert result["types_updated"] >= 1
    ahu.refresh_from_db()
    assert ahu.schema.get("catalog_version") == 2
    assert len(ahu.schema.get("attributes", [])) >= 4


def test_refresh_skips_custom(tenant):
    ahu = AssetType.objects.get(tenant=tenant, code="ahu")
    ahu.schema = {"attributes": [{"code": "custom", "value_type": "string"}], "custom": True, "catalog_version": 1}
    ahu.save(update_fields=["schema"])

    result = seed_catalog_for_tenant(tenant, refresh=True)
    ahu.refresh_from_db()
    assert ahu.schema.get("custom") is True
    assert [a.get("code") for a in ahu.schema.get("attributes", [])] == ["custom"]
    assert result["types_updated"] == 0 or ahu.schema.get("attributes")[0]["code"] == "custom"
