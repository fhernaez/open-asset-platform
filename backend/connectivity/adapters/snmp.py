"""SNMP adapter (pysnmp) — v1/v2c/v3.

Bindings: address = OID (e.g. "1.3.6.1.2.1.1.3.0"). Device bindings walk the
configured base OID and ingest values via the shared discovery pipeline.
"""
from __future__ import annotations

import logging
import time

from connectivity.adapters.base import BaseAdapter
from connectivity.models import Gateway, GatewayBinding
from connectivity.services import ingest_device_payload

logger = logging.getLogger(__name__)


class SnmpAdapter(BaseAdapter):
    protocol = "snmp"

    @classmethod
    def _session(cls, gateway: Gateway):
        from pysnmp.hlapi import CommunityData, SnmpEngine, UdpTransportTarget

        config = gateway.config or {}
        host = config.get("host")
        port = int(config.get("port") or 161)
        engine = SnmpEngine()
        if config.get("version") == "v3":
            from pysnmp.hlapi import UsmUserData

            auth = UsmUserData(
                config.get("username") or "",
                authKey=config.get("auth_password"),
            )
        else:
            auth = CommunityData(config.get("community") or "public", mpModel=1 if config.get("version") == "v1" else 0)
        transport = UdpTransportTarget((host, port), timeout=2, retries=1)
        return engine, auth, transport

    @classmethod
    def test(cls, gateway: Gateway) -> dict:
        from pysnmp.hlapi import ObjectIdentity, ObjectType, getCmd

        try:
            engine, auth, transport = cls._session(gateway)
            _error_indication, _error_status, _error_index, var_binds = next(
                getCmd(
                    engine,
                    auth,
                    transport,
                    __import__("pysnmp.hlapi").hlapi.ContextData(),
                    ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),
                )
            )
            return {"status": "connected" if var_binds else "error"}
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "detail": str(exc)[:200]}

    @classmethod
    def run_forever(cls) -> None:
        from django.utils import timezone as dj_timezone
        from pysnmp.hlapi import (
            ContextData,
            ObjectIdentity,
            ObjectType,
            getCmd,
            nextCmd,
        )

        from telemetry.storage import ingest_event

        while True:
            for gateway in Gateway.objects.filter(protocol="snmp"):
                config = gateway.config or {}
                engine, auth, transport = cls._session(gateway)
                try:
                    Gateway.objects.filter(id=gateway.id).update(connection_status="connected")
                    for binding in GatewayBinding.objects.filter(gateway=gateway):
                        if binding.binding_type == "attribute" and binding.attribute is not None:
                            _ei, _es, _ex, var_binds = next(
                                getCmd(
                                    engine,
                                    auth,
                                    transport,
                                    ContextData(),
                                    ObjectType(ObjectIdentity(binding.address)),
                                )
                            )
                            if var_binds and binding.attribute.is_active:
                                ingest_event(
                                    tenant_id=str(gateway.tenant_id),
                                    project_id=str(gateway.project_id) if gateway.project_id else None,
                                    asset_id=str(binding.asset_id),
                                    attribute_id=str(binding.attribute_id),
                                    value=var_binds[0][1].prettyPrint(),
                                    value_type=binding.attribute.value_type,
                                    observed_at=dj_timezone.now(),
                                    transport="snmp",
                                    topic=binding.address,
                                    agent_default_policy=config.get("storage_policy"),
                                    history_enabled=binding.attribute.history_enabled,
                                    history_override=binding.attribute.history_policy_override,
                                )
                        elif binding.binding_type == "device":
                            base = config.get("walk_base") or "1.3.6.1.2.1.2.2.1"
                            payload = {}
                            for _ei, _es, _ex, var_binds in nextCmd(
                                engine,
                                auth,
                                transport,
                                ContextData(),
                                ObjectType(ObjectIdentity(base)),
                                lexicographicMode=False,
                            ):
                                for oid, val in var_binds:
                                    payload[str(oid)] = val.prettyPrint()
                                if len(payload) > 50:
                                    break
                            ingest_device_payload(gateway, binding, payload, transport="snmp")
                except Exception:  # noqa: BLE001
                    logger.exception("snmp gateway %s poll failed", gateway.id)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="error")
            time.sleep(10)
