import paho.mqtt.client as mqtt
import time
import requests
import json

URL = 'https://api.openweathermap.org/data/2.5/weather?q=kolkata&appid=f7a9916652f1c84cd8201c87ec8c907c'

THINGSBOARD_HOST = 'thingsboard.e-yantra.org'
ACCESS_TOKEN = 'AVsxEDvOIn27GTKUdIpP'      # Access Token of device in thingsboard

sensor_data = {'temperature': 0, 'humidity': 0}

# Create a client instance
mqttc = mqtt.Client()

# Set access token
mqttc.username_pw_set(ACCESS_TOKEN)  # username password setting

# Connect to thingsboard using default MQTT port 1883. keepalive interval is 60 sec
# Here THINGSBOARD_HOST acts as broker
mqttc.connect(THINGSBOARD_HOST, port = 1883, keepalive = 60)

mqttc.loop_start()

try:
    while True:
        response = requests.get(URL)
        data = response.json()
        sensor_data['temperature'] = data['main']['temp'] - 273.15
        sensor_data['humidity'] = data['main']['humidity']
        print(f"Temperature: {sensor_data['temperature']} degree C, Humidity: {sensor_data['humidity']} %" )
        # Publish the data
        mqttc.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        time.sleep(10)
except KeyboardInterrupt:
    mqttc.loop_stop()
    mqttc.disconnect()