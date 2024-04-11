import paho.mqtt.client as mqtt
import time
import ssl

# Define the MQTT broker and WebSocket port
# broker_address = "localhost"
broker_address = "10.0.0.4"
# websocket_port = 8080  # Change this to the WebSocket port provided by your MQTT broker
websocket_port = 8084  # Change this to the WebSocket port provided by your MQTT broker

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
  print("Connected with result code " + str(rc))

# Subscribe to a topic upon connection
  client.subscribe("example/topic")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
  print("Received message: " + msg.payload.decode())

# Create a Paho MQTT client with WebSockets support
client = mqtt.Client(transport="websockets")

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(certfile="./device_ec_cert.pem",keyfile="./device_ec_key.pem",ca_certs="./cert.pem", tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

# Connect to the broker
client.connect(broker_address, port=websocket_port, keepalive=60)

# Start the network loop
client.loop_start()

# Publish a message to the topic
client.publish("example/topic", "Hello, MQTT!")

duration = 60
end_time = time.time() + duration

while time.time() < end_time:
  time.sleep(1)

client.loop_stop()
client.disconnect()


