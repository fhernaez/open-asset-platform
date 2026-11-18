"""MQTT adapter: connects each mqtt gateway and routes messages to bindings."""

from __future__ import annotations

import logging

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

        def on_connect(client, userdata, flags, reason_code, properties=None):
            gateway_id = userdata
            addresses = sorted({b.address for b in GatewayBinding.objects.filter(gateway_id=gateway_id)})
            for address in addresses:
                client.subscribe(address, qos=1)
            Gateway.objects.filter(id=gateway_id).update(connection_status="connected")
            logger.info("mqtt gateway %s connected; %d topics", gateway_id, len(addresses))

        def on_disconnect(client, userdata, *args, **kwargs):
            gateway_id = userdata
            Gateway.objects.filter(id=gateway_id).update(connection_status="disconnected")

        def on_message(client, userdata, msg):
            try:
                process_message(str(userdata), msg.topic, msg.payload)
            except Exception:  # noqa: BLE001
                logger.exception("ingest failed for topic %s", msg.topic)

        clients = []
        for gateway in Gateway.objects.filter(protocol="mqtt"):
            config = gateway.config or {}
            host = config.get("host")
            port = int(config.get("port") or 1883)
            if not host:
                continue
            client_id = str(config.get("client_id") or f"oap-mqtt-{gateway.id}")
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id, userdata=gateway.id)
            username = config.get("username")
            password = config.get("password")
            if username:
                client.username_pw_set(username, password)
            if config.get("tls"):
                client.tls_set()
            client.on_connect = on_connect
            client.on_disconnect = on_disconnect
            client.on_message = on_message
            try:
                client.connect(host, port, keepalive=int(config.get("keepalive") or 60))
                client.loop_start()
                clients.append(client)
            except Exception:  # noqa: BLE001
                logger.exception("mqtt gateway %s failed to connect", gateway.id)
                Gateway.objects.filter(id=gateway.id).update(connection_status="error")

        try:
            while True:
                import time  # noqa: PLC0415

                time.sleep(3600)
        except KeyboardInterrupt:  # pragma: no cover
            for client in clients:
                client.loop_stop()
