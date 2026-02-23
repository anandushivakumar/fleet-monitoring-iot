import random
import time
import json
import ssl
import os
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# load env variables
# hivemqtt broker URL, port, username and password for web-client
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# config
NUM_VEHICLES = 3
PUBLISH_INTERVAL = 5  # seconds

BASE_LAT = 25.276987
BASE_LON = 55.296249

MIN_SPEED = 40
MAX_SPEED = 140

# generate random data
def generate_vehicle_data(vehicle_id: str) -> dict:
    speed = round(random.uniform(MIN_SPEED, MAX_SPEED), 2)

    latitude = round(BASE_LAT + random.uniform(-0.02, 0.02), 6)
    longitude = round(BASE_LON + random.uniform(-0.02, 0.02), 6)

    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "vehicle_id": vehicle_id,
        "speed": speed,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp
    }

# attempt connection to MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ Cloud successfully!")
    else:
        print(f"Connection failed with code {rc}")


def main():
    if not all([MQTT_BROKER, MQTT_USERNAME, MQTT_PASSWORD]):
        print("ERROR: Missing MQTT credentials in .env file")
        return

    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    client.on_connect = on_connect

    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

    vehicle_ids = [f"VEHICLE_{i+1:03d}" for i in range(NUM_VEHICLES)]

    try:
        while True:
            for vehicle_id in vehicle_ids:
                data = generate_vehicle_data(vehicle_id)

                topic = f"fleet/vehicle/{vehicle_id}/telemetry"
                payload = json.dumps(data)

                client.publish(topic, payload)
                print(f"Published → {topic}")

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping simulator...")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()