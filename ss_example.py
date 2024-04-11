# State Store Example

from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.client import Client
import time

# Define the MQTT broker and WebSocket port
broker_address = "10.0.0.4"
port = 1883
client_id = "foo"
publish_topic = "statestore/FA9AE35F-2F64-47CD-9BFF-08E2B32A0FE8/command/invoke"
# response_topic = "clients/" + client_id + "/services/statestore/FA9AE35F-2F64-47CD-9BFF-08E2B32A0FE8/command/invoke/response"
response_topic = "clients/statestore/FA9AE35F-2F64-47CD-9BFF-08E2B32A0FE8/" + client_id + "/command/notify"
publish_payload = "Hello, MQTT!"

# RESP3 State store payloads
set_payload = b"*3\r\n$3\r\nSET\r\n$7\r\nSETKEY2\r\n$6\r\nVALUE5\r\n"
get_payload = b"*2\r\n$3\r\nGET\r\n$7\r\nSETKEY2\r\n"
lock_payload = b"*6\r\n$3\r\nSET\r\n$4\r\nLOCK\r\n$3\r\nfoo\r\n$3\r\nNEX\r\n$2\r\nPX\r\n$4\r\n1000\r\n"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties):
  print("Connected with result code " + str(rc))
  client.subscribe(response_topic)
  print("Subscribed to topic: " + response_topic)

def on_disconnect(client, userdata, rc, properties):
  print("Disconnected with result code " + str(rc))

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
  print("Received message: " + msg.payload.decode())

# Create a Paho MQTT client with WebSockets support
client = Client(client_id=client_id, protocol=5 )

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the broker
client.connect(broker_address, port=port, keepalive=60)

# Start the network loop
client.loop_start()

while client.is_connected() == False:
  time.sleep(1)

# Publish a message to the topic
properties = Properties(PacketTypes.PUBLISH)
properties.ResponseTopic = response_topic
properties.CorrelationData = b"1234"

print("Sending lock request")
# client.publish(topic=publish_topic, payload=lock_payload, properties=properties)

time.sleep(1)
print("Sending message to topic: " + publish_topic)
client.publish(topic=publish_topic, payload=set_payload, properties=properties)

# print("Sending message to topic: " + subscribe_topic)
# client.publish(topic=subscribe_topic, payload=publish_payload, properties=properties)
time.sleep(1)
print("Getting the value")
client.publish(topic=publish_topic, payload=get_payload, properties=properties, qos=1)

duration = 60
end_time = time.time() + duration

while time.time() < end_time:
  time.sleep(1)

client.loop_stop()
client.disconnect()
