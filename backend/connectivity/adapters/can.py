"""CAN bus adapter (python-can).

Bindings: address = arbitration id (hex or decimal). Signal decode from gateway
config ``signals``: {arb_id: [{name, start, length, scale, offset, signed}]}.
Device bindings ingest decoded signals via the shared discovery pipeline.
"""
from __future__ import annotations

import logging
import time

from connectivity.adapters.base import BaseAdapter
from connectivity.models import Gateway, GatewayBinding
from connectivity.services import ingest_device_payload

logger = logging.getLogger(__name__)


class CanAdapter(BaseAdapter):
    protocol = "can"

    @classmethod
    def _open(cls, gateway: Gateway):
        import can

        config = gateway.config or {}
        return can.interface.Bus(
            channel=config.get("interface") or "can0",
            interface="socketcan",
            bitrate=int(config.get("bitrate") or 500000),
        )

    @classmethod
    def test(cls, gateway: Gateway) -> dict:
        try:
            bus = cls._open(gateway)
            bus.shutdown()
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "detail": str(exc)[:200]}
        return {"status": "connected"}

    @classmethod
    def _decode(cls, data: bytes, spec: dict) -> float:
        start = int(spec.get("start", 0))
        length = int(spec.get("length", 16))
        signed = bool(spec.get("signed", False))
        raw = int.from_bytes(data, byteorder="little")
        mask = (1 << length) - 1
        value = (raw >> start) & mask
        if signed and value & (1 << (length - 1)):
            value -= 1 << length
        return value * float(spec.get("scale", 1)) + float(spec.get("offset", 0))

    @classmethod
    def run_forever(cls) -> None:
        from django.utils import timezone as dj_timezone

        from telemetry.storage import ingest_event

        while True:
            for gateway in Gateway.objects.filter(protocol="can"):
                config = gateway.config or {}
                signals = config.get("signals") or {}
                try:
                    bus = cls._open(gateway)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="connected")
                    deadline = time.time() + 10
                    while time.time() < deadline:
                        message = bus.recv(timeout=1)
                        if message is None:
                            continue
                        arb_id = str(message.arbitration_id)
                        bindings = GatewayBinding.objects.filter(gateway=gateway, address=arb_id)
                        specs = signals.get(arb_id) or []
                        for binding in bindings:
                            if binding.binding_type == "attribute" and binding.attribute is not None:
                                named = next((s for s in specs if s.get("name") == binding.mapping), None)
                                spec = named if named is not None else (specs[0] if specs else None)
                                if spec is None:
                                    continue
                                value = cls._decode(message.data, spec)
                                if binding.attribute.is_active:
                                    ingest_event(
                                        tenant_id=str(gateway.tenant_id),
                                        project_id=str(gateway.project_id) if gateway.project_id else None,
                                        asset_id=str(binding.asset_id),
                                        attribute_id=str(binding.attribute_id),
                                        value=value,
                                        value_type=binding.attribute.value_type,
                                        observed_at=dj_timezone.now(),
                                        transport="can",
                                        topic=arb_id,
                                        agent_default_policy=config.get("storage_policy"),
                                        history_enabled=binding.attribute.history_enabled,
                                        history_override=binding.attribute.history_policy_override,
                                    )
                            elif binding.binding_type == "device":
                                payload = {
                                    s.get("name") or f"sig_{i}": cls._decode(message.data, s)
                                    for i, s in enumerate(specs)
                                }
                                ingest_device_payload(gateway, binding, payload, transport="can")
                    bus.shutdown()
                except Exception:  # noqa: BLE001
                    logger.exception("can gateway %s failed", gateway.id)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="error")
            time.sleep(10)
