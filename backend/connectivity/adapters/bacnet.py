"""BACnet adapter (BAC0).

Bindings: address = "analogInput:1" style ("{objectType}:{instance}") on the
configured device. Device bindings read presentValue of configured objects and
ingest values via the shared discovery pipeline. Poll interval from gateway
config ``poll_interval``.
"""
from __future__ import annotations

import logging
import time

from connectivity.adapters.base import BaseAdapter
from connectivity.models import Gateway, GatewayBinding
from connectivity.services import ingest_device_payload

logger = logging.getLogger(__name__)


class BacnetAdapter(BaseAdapter):
    protocol = "bacnet"

    @classmethod
    def _connect(cls, gateway: Gateway):
        import BAC0

        config = gateway.config or {}
        return BAC0.lite(ip=config.get("network") or "0.0.0.0/0", port=int(config.get("port") or 47808))

    @classmethod
    def test(cls, gateway: Gateway) -> dict:
        try:
            bacnet = cls._connect(gateway)
            devices = bacnet.whois()
            bacnet.disconnect()
            return {"status": "connected" if devices else "error", "detail": f"{len(devices or [])} device(s)"}
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "detail": str(exc)[:200]}
        finally:
            try:
                bacnet.disconnect()  # noqa: B023
            except Exception:  # noqa: BLE001
                pass

    @classmethod
    def run_forever(cls) -> None:
        from django.utils import timezone as dj_timezone

        from telemetry.storage import ingest_event

        while True:
            for gateway in Gateway.objects.filter(protocol="bacnet"):
                config = gateway.config or {}
                device = str(config.get("device_instance") or 1)
                try:
                    bacnet = cls._connect(gateway)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="connected")
                    for binding in GatewayBinding.objects.filter(gateway=gateway):
                        if binding.binding_type == "attribute" and binding.attribute is not None:
                            obj_type, instance = binding.address.split(":", 1)
                            value = bacnet.read(f"{device} {obj_type} {instance} presentValue")
                            if binding.attribute.is_active:
                                ingest_event(
                                    tenant_id=str(gateway.tenant_id),
                                    project_id=str(gateway.project_id) if gateway.project_id else None,
                                    asset_id=str(binding.asset_id),
                                    attribute_id=str(binding.attribute_id),
                                    value=value,
                                    value_type=binding.attribute.value_type,
                                    observed_at=dj_timezone.now(),
                                    transport="bacnet",
                                    topic=binding.address,
                                    agent_default_policy=config.get("storage_policy"),
                                    history_enabled=binding.attribute.history_enabled,
                                    history_override=binding.attribute.history_policy_override,
                                )
                        elif binding.binding_type == "device":
                            payload = {}
                            obj_types = (
                                "analogInput", "analogOutput", "binaryInput",
                                "binaryOutput", "analogValue", "binaryValue",
                            )
                            for obj_type in obj_types:
                                try:
                                    points = bacnet.readMultiple(f"{device} {obj_type} 0 {obj_type} presentValue")
                                    for idx, value in enumerate(points, start=1):
                                        payload[f"{obj_type}:{idx}"] = value
                                except Exception:  # noqa: BLE001
                                    continue
                            ingest_device_payload(gateway, binding, payload, transport="bacnet")
                    bacnet.disconnect()
                except Exception:  # noqa: BLE001
                    logger.exception("bacnet gateway %s poll failed", gateway.id)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="error")
            time.sleep(10)
