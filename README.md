# IoT Fleet Monitoring System

An end-to-end **Internet of Things (IoT) fleet monitoring system** that simulates vehicle telemetry, detects overspeed events, stores telemetry data in the cloud, and visualizes fleet status through an interactive dashboard.

This project was developed as part of the **ECTE474 – Internet of Things** course and demonstrates a full IoT architecture integrating the **Device, Network, Cloud, and Application layers**.

---

# Project Overview

The system simulates multiple vehicles transmitting telemetry data (speed and GPS location) through an MQTT broker. The data is processed by Node-RED to detect overspeed events, store telemetry in a cloud database, and visualize fleet status in real time.

The dashboard provides live vehicle monitoring, alerts, historical analytics, and remote command capabilities.

---

# System Architecture

![System Architecture](docs/architecture.png)

### Data Flow

Vehicle Simulator (Python)
↓
MQTT Broker (HiveMQ Cloud)
↓
Node-RED Processing
↓
Cloud Storage (Firebase Realtime Database)
↓
Dashboard Visualization (Node-RED Dashboard)

---

# Features

### Vehicle Telemetry Simulation

- Simulates multiple vehicles transmitting data
- Randomized speed and GPS coordinates
- Adjustable publish interval

### MQTT Communication

- Secure TLS connection to HiveMQ Cloud
- Topic-based publish/subscribe architecture
- Real-time data streaming

### Overspeed Detection

- Detects vehicles exceeding speed threshold
- Generates overspeed alerts
- Stores alert history

### Cloud Data Storage

- Firebase Realtime Database
- Stores telemetry history
- Stores latest vehicle state

### Interactive Dashboard

- Fleet overview dashboard
- Vehicle status table
- Live vehicle speed chart
- Geographic map visualization
- Overspeed alert dashboard

### Remote Vehicle Control

- Send **SLOW_DOWN command**
- Temporarily limit vehicle speed
- Demonstrates IoT control feedback loop

---

# Technologies Used

| Layer             | Technology                 |
| ----------------- | -------------------------- |
| Device Simulation | Python                     |
| Communication     | MQTT                       |
| MQTT Broker       | HiveMQ Cloud               |
| Data Processing   | Node-RED                   |
| Cloud Storage     | Firebase Realtime Database |
| Visualization     | Node-RED Dashboard         |
| Mapping           | Leaflet.js                 |

---

# Project Structure

```
iot-fleet-monitoring/
│
├── node_red/
│   └── node_red_flow.json
│
├── src/
│   ├── simulator.py
│   ├── mqtt_client.py
│   └── config.py
│
├── docs/
│   ├── system_architecture.png
│   ├── dashboard.png
│   ├── database_structure_example.png
│   ├── map_page.png
│   ├── vehicle_monitoring.jpg
│   ├── overspeed_alerts_page.png
│   └── node_red_flow.png
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# Installation

## 1. Clone the Repository

```
git clone https://github.com/anandushivakumar/iot-fleet-monitoring.git
cd iot-fleet-monitoring
```

---

## 2. Install Python Dependencies

```
pip install -r requirements.txt
```

Dependencies:

- paho-mqtt
- python-dotenv

---

## 3. Configure MQTT Credentials

Create a `.env` file in the root directory.

```
MQTT_BROKER=your_hivemq_cloud_url
MQTT_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password
```

---

## 4. Start the Vehicle Simulator

```
python src/simulator.py
```

The simulator will publish telemetry data every **5 seconds**.

Example output:

```
Published → fleet/vehicle/VEHICLE_001/telemetry
Published → fleet/vehicle/VEHICLE_002/telemetry
Published → fleet/vehicle/VEHICLE_003/telemetry
```

---

## 5. Start Node-RED

Run:

```
node-red
```

Open Node-RED:

```
http://localhost:1880
```

Import the flow file:

```
node_red/node_red_flow.json
```

---

## 6. Open the Dashboard

```
http://localhost:1880/dashboard
```

---

# Authors

Anandu Shivakumar - 7543207
Mohamed Shaaban - 7821918
