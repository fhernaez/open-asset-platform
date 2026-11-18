"""Multi-protocol connectivity worker.

Runs one adapter per gateway protocol (registry below). Only the MQTT adapter
is implemented today (P0); Modbus/OPC-UA/BACnet/SNMP/CAN are SPECIFIED until
their adapters land (never presented as functional).
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
        for protocol, adapter_cls in ADAPTERS.items():
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
