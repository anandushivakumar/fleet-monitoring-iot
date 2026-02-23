import ssl
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to HiveMQ Cloud successfully!")
        else:
            print(f"Connection failed with code {reason_code}")

    def connect(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.client.loop_start()

    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()