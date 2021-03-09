import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'thingsboard.e-yantra.org'
ACCESS_TOKEN = 'AVsxEDvOIn27GTKUdIpP'      # Access Token of device in thingsboard

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("v1/devices/me/rpc/request/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)
    #print(data)
    if data['method'] == 'setValue':
        print('Current Status of Switch is : ', str(data['params']))
        mqttc.publish('v1/devices/me/attributes', json.dumps({'prevState': str(not data['params'])}), 1)


# Create a client instance
mqttc = mqtt.Client()

# Register connect callback 
mqttc.on_connect = on_connect

# Register publish message callback
mqttc.on_message = on_message

# Set access token
mqttc.username_pw_set(ACCESS_TOKEN)  # username password setting

# Connect to thingsboard using default MQTT port 1883. keepalive interval is 60 sec
# Here THINGSBOARD_HOST acts as broker
mqttc.connect(THINGSBOARD_HOST, port = 1883, keepalive = 60)

mqttc.loop_forever()