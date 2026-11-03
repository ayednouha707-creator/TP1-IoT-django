import argparse
import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

#MQTT config
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"


#publisher interval in seconds
parser = argparse.ArgumentParser()
parser.add_argument("--interval", type=float, default=1.0)
args = parser.parse_args()
INTERVAL = args.interval



def generate_mesure():
    """Generate a random temperature and humidity measurement."""
   
    return {
        "value": round(random.uniform(15.0, 35.0), 2),
        "date_prise": datetime.now(timezone.utc).isoformat()

    }

def main():
    """Main function to publish sensor data to MQTT broker."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    print(f"connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.loop_start()

    
    try:
        while True:
            mesure = generate_mesure()

            payload = json.dumps(mesure)

            client.publish(MQTT_TOPIC, payload)

            print(f"Published: {payload} to topic: {MQTT_TOPIC}")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping publisher...")

    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()