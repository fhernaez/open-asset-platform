"""MQTT adapter: connects each mqtt gateway and routes messages to bindings.

The worker periodically re-syncs gateways and bindings so that gateways/bindings
created or edited after startup are picked up without a restart, and
``connection_status`` stays authoritative (real worker state).
"""
from __future__ import annotations

import logging
import time

from connectivity.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)


class MqttAdapter(BaseAdapter):
    protocol = "mqtt"

    @classmethod
    def run_forever(cls) -> None:
        try:
            import paho.mqtt.client as mqtt  # noqa: PLC0415
        except ImportError:  # pragma: no cover
            logger.error("paho-mqtt is not installed; MQTT adapter disabled.")
            return

        from connectivity.models import Gateway, GatewayBinding
        from connectivity.services import process_message

        clients: dict[str, mqtt.Client] = {}

        def subscribe_bindings(client, gateway_id):
            addresses = sorted({b.address for b in GatewayBinding.objects.filter(gateway_id=gateway_id)})
            for address in addresses:
                client.subscribe(address, qos=1)

        def on_connect(client, userdata, flags, reason_code, properties=None):
            gateway_id = userdata
            subscribe_bindings(client, gateway_id)
            Gateway.objects.filter(id=gateway_id).update(connection_status="connected")
            logger.info("mqtt gateway %s connected", gateway_id)

        def on_disconnect(client, userdata, *args, **kwargs):
            gateway_id = userdata
            Gateway.objects.filter(id=gateway_id).update(connection_status="disconnected")

        def on_message(client, userdata, msg):
            try:
                process_message(str(userdata), msg.topic, msg.payload)
            except Exception:  # noqa: BLE001
                logger.exception("ingest failed for topic %s", msg.topic)

        def sync() -> None:
            """Connect new gateways, disconnect removed ones, refresh subscriptions."""
            seen: set[str] = set()
            for gateway in Gateway.objects.filter(protocol="mqtt"):
                seen.add(str(gateway.id))
                config = gateway.config or {}
                host = config.get("host")
                if not host:
                    Gateway.objects.filter(id=gateway.id).update(connection_status="error")
                    continue
                port = int(config.get("port") or 1883)
                if str(gateway.id) in clients:
                    subscribe_bindings(clients[str(gateway.id)], gateway.id)
                    continue
                client_id = str(config.get("client_id") or f"oap-mqtt-{gateway.id}")
                client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id, userdata=gateway.id)
                username = config.get("username")
                if username:
                    client.username_pw_set(username, config.get("password"))
                if config.get("tls"):
                    client.tls_set()
                client.on_connect = on_connect
                client.on_disconnect = on_disconnect
                client.on_message = on_message
                try:
                    client.connect(host, port, keepalive=int(config.get("keepalive") or 60))
                    client.loop_start()
                    clients[str(gateway.id)] = client
                except Exception:  # noqa: BLE001
                    logger.exception("mqtt gateway %s failed to connect", gateway.id)
                    Gateway.objects.filter(id=gateway.id).update(connection_status="error")

            for gateway_id in list(clients):
                if gateway_id not in seen:
                    clients[gateway_id].loop_stop()
                    clients[gateway_id].disconnect()
                    del clients[gateway_id]

        try:
            while True:
                sync()
                time.sleep(10)
        except KeyboardInterrupt:  # pragma: no cover
            for client in clients.values():
                client.loop_stop()
