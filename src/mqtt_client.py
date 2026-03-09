import ssl
import json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD

# wrapper class for paho MQTT client
# handles connection to MQTT broker, authentication, subscribing, publishing, handling messages
class MQTTClient:
    def __init__(self, on_message_callback=None):
        # creat MQTT client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        
        # set MQTT credentials
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        
        # enable TLS encrytion
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

        # store external callback to process incoming messages
        self.on_message_callback = on_message_callback

        # assign internal callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # callback when client connects to MQTT broker
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0: # successful connection
            print("Connected to HiveMQ Cloud successfully!")
        else: # connection failed
            print(f"Connection failed with code {reason_code}")

    # callback when message received
    def on_message(self, client, userdata, msg):
        if not self.on_message_callback: # no external callback, ignore
            return
        try:
            # decode incoming MQTT payload from bytes to JSON
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception:
            # ignore malformed payloads
            return
        try:
            # pass topic and parsed payload to external handler
            self.on_message_callback(msg.topic, payload)
        except Exception:
            # prevent callback errors from crashing the MQTT loop
            return

    # connect to MQTT broker and start network loop
    def connect(self): 
        # establish connection to broker
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.client.loop_start() # start network loop

    # subscribe to MQTT topic
    def subscribe(self, topic: str, qos: int = 0):
        self.client.subscribe(topic, qos=qos)

    # publish MQTT message
    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload)

    # disconnect from MQTT broker
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()