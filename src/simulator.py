import random
import time
import json
from datetime import datetime, timezone
from mqtt_client import MQTTClient

NUM_VEHICLES = 3 # number of vehicles 
PUBLISH_INTERVAL = 5 # seconds 

# base geographical coordinates
BASE_LAT = 25.276987
BASE_LON = 55.296249

# predefined speed thresholds
MIN_SPEED = 40
MAX_SPEED = 140

# default parameters for when slow down command is used
SLOWDOWN_DEFAULT_TARGET = 60.0 # km/h
SLOWDOWN_DEFAULT_DURATION = 20 # seconds

# dictionary to store speed limits
speed_caps = {} 

# function to generate telemetry data for the vehicle
# speed, GPS location, timestamp
def generate_vehicle_data(vehicle_id: str) -> dict:

    # generate random speed
    speed = round(random.uniform(MIN_SPEED, MAX_SPEED), 2)

    # check if slow down command active
    now = time.time()
    cap_info = speed_caps.get(vehicle_id)
    if cap_info:
        # if comman active, limit speed
        if now <= cap_info["until"]:
            speed = round(min(speed, cap_info["cap"]), 2)
        else:
            # remove expired speed cap
            speed_caps.pop(vehicle_id, None)

    # generate random GPS coordinates
    latitude = round(BASE_LAT + random.uniform(-0.02, 0.02), 6)
    longitude = round(BASE_LON + random.uniform(-0.02, 0.02), 6)

    # generate timestamp
    timestamp = datetime.now(timezone.utc).isoformat()

    # return telemetry data
    return {
        "vehicle_id": vehicle_id,
        "speed": speed,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp
    }

# function to handle slow down command
# handles incoming MQTT commands from Node-RED
def on_command(topic: str, payload: dict):

    # split topic string to extract vehicle ID
    parts = topic.split("/")

    # validate topic format
    if len(parts) < 4:
        return
    if parts[0] != "fleet" or parts[1] != "vehicle" or parts[3] != "command":
        return

    # extract vehicle ID from topic
    vehicle_id = parts[2]

    # only process slow down commands
    if payload.get("command") != "SLOW_DOWN":
        return

    # read command parameters or use default values
    cap = float(payload.get("target_speed", SLOWDOWN_DEFAULT_TARGET))
    duration = int(payload.get("duration_sec", SLOWDOWN_DEFAULT_DURATION))

    # store speed cap and expiration time
    speed_caps[vehicle_id] = {"cap": cap, "until": time.time() + duration}
    
    # log command execution
    print(f"[COMMAND] {vehicle_id} SLOW_DOWN -> {cap} for {duration}s", flush=True)


# main function to:
# 1. connect to MQTT broker
# 2. subscribe to command topic
# 3. publish telemetry data periodically
def main():

    # init MQTT client
    mqtt_client = MQTTClient(on_message_callback=on_command)
    
    # connect to HiveMQ broker
    mqtt_client.connect()

    # subscribe to command topic for all vehicles
    mqtt_client.subscribe("fleet/vehicle/+/command")

    # generate vehicle IDs
    vehicle_ids = [f"VEHICLE_{i+1:03d}" for i in range(NUM_VEHICLES)]

    # start sim 
    print("Simulator started", flush=True)
    print(f"Publishing {NUM_VEHICLES} vehicles every {PUBLISH_INTERVAL} seconds", flush=True)

    try:
        while True:
            # generate and publish telemetry data for each vehicle
            for vehicle_id in vehicle_ids:

                # generate simulated data
                data = generate_vehicle_data(vehicle_id)

                # MQTT topic for telemetry
                topic = f"fleet/vehicle/{vehicle_id}/telemetry"

                # convert data to JSON
                payload = json.dumps(data)

                # publish telemetry
                mqtt_client.publish(topic, payload)
                print(f"Published → {topic} | {payload}", flush=True) # log message

            time.sleep(PUBLISH_INTERVAL) # wait before next publish

    except KeyboardInterrupt:
        print("\nStopping simulator...", flush=True) # stop sim
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()