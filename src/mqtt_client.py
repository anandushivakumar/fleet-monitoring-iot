import ssl
import json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD


class MQTTClient:
    def __init__(self, on_message_callback=None):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

        self.on_message_callback = on_message_callback

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to HiveMQ Cloud successfully!")
        else:
            print(f"Connection failed with code {reason_code}")

    def on_message(self, client, userdata, msg):
        if not self.on_message_callback:
            return
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception:
            return
        try:
            self.on_message_callback(msg.topic, payload)
        except Exception:
            return

    def connect(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.client.loop_start()

    def subscribe(self, topic: str, qos: int = 0):
        self.client.subscribe(topic, qos=qos)

    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()