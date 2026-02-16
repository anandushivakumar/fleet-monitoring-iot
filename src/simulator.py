import random
import time
import json
from datetime import datetime, timezone

# config
NUM_VEHICLES = 50 # number of vehicles tracked
PUBLISH_INTERVAL = 5  # publish data every 5s

# Base GPS location (ex: depot)
BASE_LAT = 25.276987
BASE_LON = 55.296249

# Speed limits (km/h)
MIN_SPEED = 40 
MAX_SPEED = 140 


def generate_vehicle_data(vehicle_id: str) -> dict:
    # generate simulated telemetry data for a single vehicle.
    speed = round(random.uniform(MIN_SPEED, MAX_SPEED), 2)

    # gmall random movement around base location
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
    print("Simulator Start")
    print(f"Simulating {NUM_VEHICLES} vehicles")

    vehicle_ids = [f"VEHICLE_{i+1:03d}" for i in range(NUM_VEHICLES)]

    try:
        while True:
            for vehicle_id in vehicle_ids:
                data = generate_vehicle_data(vehicle_id)
                print(json.dumps(data))
            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    main()