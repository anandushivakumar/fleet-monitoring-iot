import random
import time
import json
from datetime import datetime, timezone
from mqtt_client import MQTTClient

# config for sim
NUM_VEHICLES = 3
PUBLISH_INTERVAL = 5  # every 5 seconds

BASE_LAT = 25.276987
BASE_LON = 55.296249

MIN_SPEED = 40
MAX_SPEED = 140


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


def main():
    mqtt_client = MQTTClient()
    mqtt_client.connect()

    vehicle_ids = [f"VEHICLE_{i+1:03d}" for i in range(NUM_VEHICLES)]

    try:
        while True:
            for vehicle_id in vehicle_ids:
                data = generate_vehicle_data(vehicle_id)

                topic = f"fleet/vehicle/{vehicle_id}/telemetry"
                payload = json.dumps(data)

                mqtt_client.publish(topic, payload)
                print(f"Published → {topic}")

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping simulator...")
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()