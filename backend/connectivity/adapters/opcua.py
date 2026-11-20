"""OPC-UA adapter (asyncua).

Bindings: address = NodeId (e.g. "ns=2;i=5"). Device bindings browse child nodes
of the configured root and ingest values so the shared discovery pipeline
proposes attributes. Poll interval from gateway config ``poll_interval``.
"""
from __future__ import annotations

import asyncio
import logging
import time

from connectivity.adapters.base import BaseAdapter
from connectivity.models import Gateway, GatewayBinding
from connectivity.services import ingest_device_payload

logger = logging.getLogger(__name__)


class OpcuaAdapter(BaseAdapter):
    protocol = "opcua"

    @classmethod
    def _connect(cls, gateway: Gateway):
        from asyncua import Client

        config = gateway.config or {}
        return Client(url=config.get("endpoint_url"), timeout=float(config.get("connect_timeout") or 5))

    @classmethod
    def test(cls, gateway: Gateway) -> dict:
        try:
            client = cls._connect(gateway)

            async def probe():
                async with client:
                    await client.get_root_node()

            asyncio.run(probe())
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "detail": str(exc)[:200]}
        return {"status": "connected"}

    @classmethod
    def run_forever(cls) -> None:
        from django.utils import timezone as dj_timezone

        from telemetry.storage import ingest_event

        while True:
            for gateway in Gateway.objects.filter(protocol="opcua"):
                config = gateway.config or {}
                try:
                    client = cls._connect(gateway)

                    async def poll(client=client, gateway=gateway, config=config):
                        async with client:
                            Gateway.objects.filter(id=gateway.id).update(connection_status="connected")
                            for binding in GatewayBinding.objects.filter(gateway=gateway):
                                if binding.binding_type == "attribute" and binding.attribute is not None:
                                    node = client.get_node(binding.address)
                                    value = await node.read_value()
                                    if binding.attribute.is_active:
                                        ingest_event(
                                            tenant_id=str(gateway.tenant_id),
                                            project_id=str(gateway.project_id) if gateway.project_id else None,
                                            asset_id=str(binding.asset_id),
                                            attribute_id=str(binding.attribute_id),
                                            value=value,
                                            value_type=binding.attribute.value_type,
                                            observed_at=dj_timezone.now(),
                                            transport="opcua",
                                            topic=binding.address,
                                            agent_default_policy=config.get("storage_policy"),
                                            history_enabled=binding.attribute.history_enabled,
                                            history_override=binding.attribute.history_policy_override,
                                        )
                                elif binding.binding_type == "device":
                                    root = config.get("browse_root")
                                    if root:
                                        payload = {}
                                        async for child in client.nodes.get_node(root).get_children():
                                            try:
                                                payload[child.nodeid.to_string()] = await child.read_value()
                                            except Exception:  # noqa: BLE001
                                                continue
                                        ingest_device_payload(gateway, binding, payload, transport="opcua")

                    asyncio.run(poll())
                except Exception:  # noqa: BLE001
                    logger.exception("opcua gateway %s poll failed", gateway.id)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="error")
            time.sleep(10)
