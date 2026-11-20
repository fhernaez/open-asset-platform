"""Semantic projection: assets as RDF (Brick/Haystack/81346) + SHACL validation.

Offline projection (ADR-018): never in the write path. Uses rdflib/pyshacl,
imported lazily so the core app has no hard dependency at runtime.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

BRICK = "https://brickschema.org/schema/Brick#"
HAYSTACK = "https://project-haystack.org/def/"
OAP = "https://oap.local/schema#"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


def _iri(prefix: str, term: str) -> str:
    return f"{prefix}{term.replace(' ', '_')}"


def build_graph(tenant=None) -> str:
    """Build the RDF projection as turtle text (one asset graph per asset)."""
    from rdflib import Graph, Literal, Namespace, URIRef

    from assets.models import Asset, AssetAttribute, AssetRelationship

    graph = Graph()
    BRICK_NS = Namespace(BRICK)
    OAP_NS = Namespace(OAP)
    graph.bind("brick", BRICK_NS)
    graph.bind("oap", OAP_NS)

    assets = Asset.objects.select_related("asset_type").prefetch_related("attributes")
    if tenant is not None:
        assets = assets.filter(tenant=tenant)
    for asset in assets:
        node = URIRef(f"{OAP}asset/{asset.id}")
        classes = (asset.metadata or {}).get("brick") or []
        if not classes and asset.asset_type is not None:
            classes = (asset.asset_type.schema or {}).get("brick") or []
        if not classes:
            classes = ["Asset"]
        for cls in classes:
            graph.add((node, URIRef(RDF_TYPE), URIRef(_iri(BRICK, cls))))
        graph.add((node, BRICK_NS["label"], Literal(asset.name)))
        for aspect, value in (asset.designations or {}).items():
            if isinstance(value, dict):
                graph.add(
                    (
                        node,
                        OAP_NS["designation"],
                        Literal(f"{aspect}:{value.get('code')}-{value.get('occurrence')}"),
                    )
                )
        for attribute in AssetAttribute.objects.filter(asset=asset):
            point = URIRef(f"{OAP}point/{attribute.id}")
            graph.add((node, BRICK_NS["hasPoint"], point))
            brick_classes = (attribute.metadata or {}).get("brick") or ["Point"]
            for cls in brick_classes:
                graph.add((point, URIRef(RDF_TYPE), URIRef(_iri(BRICK, cls))))
            haystack_tags = (attribute.metadata or {}).get("haystack") or []
            for tag in haystack_tags:
                graph.add((point, URIRef(_iri(HAYSTACK, tag)), Literal(True)))
        for relation in AssetRelationship.objects.filter(tenant=asset.tenant, source=asset):
            target = URIRef(f"{OAP}asset/{relation.target_id}")
            graph.add((node, BRICK_NS[relation.relation_type], target))
    return graph.serialize(format="turtle")


def validate_with_shacl(tenant=None) -> tuple[int, list[str]]:
    """Validate the projection with SHACL shapes generated from manifest rules."""
    import pyshacl
    from rdflib import BNode, Graph, Literal, Namespace, URIRef

    from assets.models import AssetType

    data = Graph().parse(data=build_graph(tenant=tenant), format="turtle")
    shapes = Graph()
    BRICK_NS = Namespace(BRICK)
    SH = Namespace("http://www.w3.org/ns/shacl#")
    shapes.bind("sh", SH)
    shapes.bind("brick", BRICK_NS)
    types = AssetType.objects.all()
    if tenant is not None:
        types = types.filter(tenant=tenant)
    for asset_type in types:
        rules = (asset_type.schema or {}).get("rules") or {}
        if not rules:
            continue
        classes = (asset_type.schema or {}).get("brick") or []
        if not classes:
            continue
        shape = URIRef(f"{OAP}shape/{asset_type.code}")
        for cls in classes:
            shapes.add((shape, SH["targetClass"], URIRef(_iri(BRICK, cls))))
        for _code in rules.get("required_attributes") or []:
            prop = BNode()
            shapes.add((shape, SH["property"], prop))
            shapes.add((prop, SH["path"], BRICK_NS["hasPoint"]))
            shapes.add((prop, SH["minCount"], Literal(1)))
        for rel_rule in rules.get("required_relations") or []:
            prop = BNode()
            shapes.add((shape, SH["property"], prop))
            shapes.add((prop, SH["path"], BRICK_NS[rel_rule.get("relation", "")]))
            shapes.add((prop, SH["minCount"], Literal(1)))
    conforms, _report_graph, report_text = pyshacl.validate(
        data,
        shacl_graph=shapes,
        inference="rdfs",
    )
    issues = [line for line in report_text.splitlines() if "Violation" in line]
    return (0 if conforms else 1), issues
