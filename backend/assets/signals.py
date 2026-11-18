"""Signals: seed the built-in catalog when a tenant is created."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def seed_catalog_on_tenant_create(sender, instance, created, **kwargs) -> None:
    if not created:
        return
    from assets.services import seed_catalog_for_tenant

    try:
        result = seed_catalog_for_tenant(instance)
        logger.info("catalog seeded for tenant %s: %s", instance.slug, result)
    except Exception:  # noqa: BLE001 - seeding must never break tenant creation
        logger.exception("failed to seed catalog for tenant %s", instance.slug)
