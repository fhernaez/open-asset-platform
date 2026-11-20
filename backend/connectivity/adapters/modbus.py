"""Modbus RTU/TCP adapter (pymodbus).

Bindings: address = register number (int) or "holding:N". Poll interval from
gateway config ``poll_interval`` (seconds). Device bindings scan a configurable
range (``scan_start``/``scan_count``) and ingest values as a payload dict so the
shared discovery pipeline proposes attributes.
"""
from __future__ import annotations

import logging
import time

from connectivity.adapters.base import BaseAdapter
from connectivity.models import Gateway, GatewayBinding
from connectivity.services import ingest_device_payload

logger = logging.getLogger(__name__)


class ModbusAdapter(BaseAdapter):
    protocols = ["modbus-rtu", "modbus-tcp"]

    @classmethod
    def _client(cls, gateway: Gateway):
        from pymodbus.client import ModbusSerialClient, ModbusTcpClient

        config = gateway.config or {}
        timeout = float(config.get("timeout") or 3)
        if gateway.protocol == "modbus-rtu":
            return ModbusSerialClient(
                port=config.get("serial_port") or "/dev/ttyUSB0",
                baudrate=int(config.get("baud") or 9600),
                parity=(config.get("parity") or "N")[0],
                stopbits=int(config.get("stop_bits") or 1),
                bytesize=int(config.get("byte_size") or 8),
                timeout=timeout,
            )
        return ModbusTcpClient(host=config.get("host"), port=int(config.get("port") or 502), timeout=timeout)

    @classmethod
    def _unit(cls, gateway: Gateway) -> int:
        return int((gateway.config or {}).get("unit_id") or 1)

    @classmethod
    def test(cls, gateway: Gateway) -> dict:
        try:
            client = cls._client(gateway)
            connected = bool(client.connect())
            client.close()
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "detail": str(exc)[:200]}
        return {"status": "connected" if connected else "error"}

    @classmethod
    def run_forever(cls) -> None:
        from telemetry.storage import ingest_event

        while True:
            for gateway in Gateway.objects.filter(protocol__in=cls.protocols):
                config = gateway.config or {}
                client = cls._client(gateway)
                unit = cls._unit(gateway)
                try:
                    if not client.connect():
                        Gateway.objects.filter(id=gateway.id).update(connection_status="error")
                        continue
                    Gateway.objects.filter(id=gateway.id).update(connection_status="connected")
                    for binding in GatewayBinding.objects.filter(gateway=gateway):
                        if binding.binding_type == "attribute" and binding.attribute is not None:
                            register = cls._parse_register(binding.address)
                            result = client.read_holding_registers(register, count=1, slave=unit)
                            value = result.registers[0] if not result.isError() else None
                            if value is None or not binding.attribute.is_active:
                                continue
                            ingest_event(
                                tenant_id=str(gateway.tenant_id),
                                project_id=str(gateway.project_id) if gateway.project_id else None,
                                asset_id=str(binding.asset_id),
                                attribute_id=str(binding.attribute_id),
                                value=value,
                                value_type=binding.attribute.value_type,
                                observed_at=__import__("django").utils.timezone.now(),
                                transport=gateway.protocol,
                                topic=binding.address,
                                agent_default_policy=config.get("storage_policy"),
                                history_enabled=binding.attribute.history_enabled,
                                history_override=binding.attribute.history_policy_override,
                            )
                        elif binding.binding_type == "device":
                            start = int(config.get("scan_start") or 0)
                            count = int(config.get("scan_count") or 20)
                            result = client.read_holding_registers(start, count=count, slave=unit)
                            if result.isError():
                                continue
                            payload = {f"reg_{start + i}": v for i, v in enumerate(result.registers)}
                            ingest_device_payload(gateway, binding, payload, transport=gateway.protocol)
                except Exception:  # noqa: BLE001
                    logger.exception("modbus gateway %s poll failed", gateway.id)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="error")
                finally:
                    client.close()
            time.sleep(10)

    @classmethod
    def _parse_register(cls, address: str) -> int:
        if address.startswith("holding:"):
            return int(address.split(":", 1)[1])
        return int(address)
