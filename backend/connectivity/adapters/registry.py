"""Adapter registry: one adapter class per gateway protocol."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from connectivity.adapters.base import BaseAdapter


def _load_registry() -> dict[str, type[BaseAdapter]]:
    from connectivity.adapters.mqtt import MqttAdapter

    adapters: dict[str, type[BaseAdapter]] = {"mqtt": MqttAdapter}
    # P2: modbus, opcua, bacnet, snmp, can — SPECIFIED in REQUIREMENTS (OAP-CON-005).
    return adapters


ADAPTERS = _load_registry()
