import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

client = mqtt.Client()
client.connect("localhost", 1883, 60)

for i in range(10):
    data = {
        "suhu": round(random.uniform(20.0, 36.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "lux": random.randint(10, 40),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    client.publish("esp32/sensor", json.dumps(data))
    print("📤 Published:", data)
    time.sleep(1)

client.disconnect()