"""Semantic projection tests: RDF build + SHACL validation (ADR-018)."""

from __future__ import annotations

from assets.models import Asset, AssetAttribute, AssetType


def test_build_graph_projects_assets_and_points(tenant, project):
    asset_type = AssetType.objects.create(
        tenant=tenant,
        project=project,
        code="chiller-sem",
        name="Chiller Sem",
        kind="asset",
        schema={
            "brick": ["chiller"],
            "haystack": ["chiller"],
            "rules": {"required_attributes": ["temp"]},
        },
    )
    asset = Asset.objects.create(
        tenant=tenant,
        project=project,
        name="CH-1",
        external_ref="CH-1",
        asset_type=asset_type,
        designations={"function": {"code": "E1", "occurrence": 1}},
    )
    AssetAttribute.objects.create(
        tenant=tenant, project=project, asset=asset, code="temp", name="Temp", value_type="number", is_active=True,
    )

    from assets.semantics import build_graph

    turtle = build_graph(tenant=tenant)
    assert "CH-1" in turtle
    assert "chiller" in turtle
    assert "hasPoint" in turtle
    assert "designation" in turtle


def test_validate_with_shacl_conforms(tenant, project):
    asset_type = AssetType.objects.create(
        tenant=tenant,
        project=project,
        code="chiller-shacl",
        name="Chiller SHACL",
        kind="asset",
        schema={"brick": ["chiller"], "rules": {"required_attributes": ["temp"]}},
    )
    asset = Asset.objects.create(
        tenant=tenant, project=project, name="CH-2", external_ref="CH-2", asset_type=asset_type
    )
    AssetAttribute.objects.create(
        tenant=tenant, project=project, asset=asset, code="temp", name="Temp", value_type="number", is_active=True,
    )

    from assets.semantics import validate_with_shacl

    code, issues = validate_with_shacl(tenant=tenant)
    assert code == 0, issues


def test_validate_with_shacl_reports_missing_attribute(tenant, project):
    asset_type = AssetType.objects.create(
        tenant=tenant,
        project=project,
        code="chiller-gap",
        name="Chiller Gap",
        kind="asset",
        schema={"brick": ["chiller"], "rules": {"required_attributes": ["temp"]}},
    )
    Asset.objects.create(tenant=tenant, project=project, name="CH-3", external_ref="CH-3", asset_type=asset_type)

    from assets.semantics import validate_with_shacl

    code, issues = validate_with_shacl(tenant=tenant)
    assert code == 1
    assert issues
