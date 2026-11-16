"""Direct MQTT ingestion worker (no Node-RED).

Connects to the broker, subscribes to every agent binding topic and drives the
telemetry ingestion pipeline on each message. Authentication/authorization is
enforced upstream by the broker ACL and re-checked by tenant scoping at ingest.
"""

from __future__ import annotations

import logging
import os
from urllib.parse import urlparse

from django.core.management.base import BaseCommand

from mqtt.models import MqttBinding
from mqtt.services import process_message

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the direct MQTT ingestion worker."

    def handle(self, *args, **options):
        try:
            import paho.mqtt.client as mqtt  # noqa: PLC0415
        except ImportError:  # pragma: no cover
            self.stderr.write("paho-mqtt is not installed; cannot run MQTT worker.")
            raise

        broker_url = os.environ.get("MQTT_BROKER_URL", "mqtt://mqtt-broker:1883")
        parsed = urlparse(broker_url)
        host = parsed.hostname or "mqtt-broker"
        port = parsed.port or 1883
        client_id = os.environ.get("MQTT_WORKER_CLIENT_ID", "oap-telemetry-worker")

        def on_connect(client, userdata, flags, reason_code, properties=None):
            bindings = MqttBinding.objects.select_related("agent").all()
            topics = sorted({b.subscribe_topic for b in bindings})
            for topic in topics:
                client.subscribe(topic, qos=1)
            logger.info("MQTT worker connected; subscribed to %d topics", len(topics))

        def on_message(client, userdata, msg):
            bindings = MqttBinding.objects.select_related("agent").filter(subscribe_topic=msg.topic)
            for binding in bindings:
                try:
                    process_message(str(binding.agent_id), msg.topic, msg.payload)
                except Exception:  # noqa: BLE001
                    logger.exception("Ingest failed for topic %s", msg.topic)

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(host, port, keepalive=60)
        client.loop_forever()
