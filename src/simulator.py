import random
import time
import json
from datetime import datetime, timezone
from mqtt_client import MQTTClient

NUM_VEHICLES = 3
PUBLISH_INTERVAL = 5

BASE_LAT = 25.276987
BASE_LON = 55.296249

MIN_SPEED = 40
MAX_SPEED = 140

SLOWDOWN_DEFAULT_TARGET = 60.0
SLOWDOWN_DEFAULT_DURATION = 20

speed_caps = {}


def generate_vehicle_data(vehicle_id: str) -> dict:
    speed = round(random.uniform(MIN_SPEED, MAX_SPEED), 2)

    now = time.time()
    cap_info = speed_caps.get(vehicle_id)
    if cap_info:
        if now <= cap_info["until"]:
            speed = round(min(speed, cap_info["cap"]), 2)
        else:
            speed_caps.pop(vehicle_id, None)

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


def on_command(topic: str, payload: dict):
    parts = topic.split("/")
    if len(parts) < 4:
        return
    if parts[0] != "fleet" or parts[1] != "vehicle" or parts[3] != "command":
        return

    vehicle_id = parts[2]
    if payload.get("command") != "SLOW_DOWN":
        return

    cap = float(payload.get("target_speed", SLOWDOWN_DEFAULT_TARGET))
    duration = int(payload.get("duration_sec", SLOWDOWN_DEFAULT_DURATION))
    speed_caps[vehicle_id] = {"cap": cap, "until": time.time() + duration}
    print(f"[COMMAND] {vehicle_id} SLOW_DOWN -> {cap} for {duration}s")


def main():
    mqtt_client = MQTTClient(on_message_callback=on_command)
    mqtt_client.connect()

    mqtt_client.subscribe("fleet/vehicle/+/command")

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