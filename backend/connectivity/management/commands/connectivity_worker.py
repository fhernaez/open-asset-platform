"""Multi-protocol connectivity worker.

Runs one adapter worker per adapter class (MQTT, Modbus RTU/TCP, OPC-UA,
BACnet, SNMP, CAN). Workers re-sync gateways/bindings each loop so runtime
edits are picked up without restart, and ``connection_status`` stays
authoritative (real worker state).
"""

from __future__ import annotations

import logging
import threading

from django.core.management.base import BaseCommand

from connectivity.adapters.registry import ADAPTERS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run connectivity adapters for all gateways (multi-protocol worker)."

    def handle(self, *args, **options):
        threads: list[threading.Thread] = []
        seen: set[type] = set()
        for protocol, adapter_cls in ADAPTERS.items():
            if adapter_cls in seen:
                continue
            seen.add(adapter_cls)
            thread = threading.Thread(
                target=adapter_cls.run_forever,
                name=f"connectivity-{protocol}",
                daemon=True,
            )
            thread.start()
            threads.append(thread)
            logger.info("adapter %s started", protocol)
        if not threads:
            self.stderr.write("no adapters registered; nothing to run")
            return
        for thread in threads:
            thread.join()
