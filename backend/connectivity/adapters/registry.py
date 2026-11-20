"""Adapter registry: one adapter class per gateway protocol."""
from __future__ import annotations


def _load_registry() -> dict[str, type]:
    from connectivity.adapters.bacnet import BacnetAdapter
    from connectivity.adapters.can import CanAdapter
    from connectivity.adapters.modbus import ModbusAdapter
    from connectivity.adapters.mqtt import MqttAdapter
    from connectivity.adapters.opcua import OpcuaAdapter
    from connectivity.adapters.snmp import SnmpAdapter

    adapters: dict[str, type] = {
        "mqtt": MqttAdapter,
        "modbus-rtu": ModbusAdapter,
        "modbus-tcp": ModbusAdapter,
        "opcua": OpcuaAdapter,
        "bacnet": BacnetAdapter,
        "snmp": SnmpAdapter,
        "can": CanAdapter,
    }
    return adapters


ADAPTERS = _load_registry()
