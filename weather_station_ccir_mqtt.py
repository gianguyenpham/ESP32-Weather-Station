# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import busio
import board
from board import *
import adafruit_sht4x
import adafruit_scd30

# Add settings.toml to your filesystem CIRCUITPY_WIFI_SSID and CIRCUITPY_WIFI_PASSWORD keys
# with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.

# Set your Adafruit IO Username, Key and Port in settings.toml
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = os.getenv("aio_username")
aio_key = os.getenv("aio_key")

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(
    os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
)
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}!")
### Feeds ###

# Setup a feed named 'Temperature' for publishing to a feed
temperature_feed = aio_username + "/feeds/temperature"

# Setup a feed named 'Humidity' for publishing to a feed
humidity_feed = aio_username + "/feeds/humidity"

# Setup a feed named 'CO2' for publishing to a feed
co2_feed = aio_username + "/feeds/co2"

# Setup a feed named 'onoff' for subscribing to changes
#onoff_feed = aio_username + "/feeds/onoff"

### Code ###


# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    #print(f"Connected to Adafruit IO! Listening for topic changes on {onoff_feed}")
    print(f"Connected to Adafruit IO!")
    # Subscribe to all changes on the onoff_feed.
    #client.subscribe(onoff_feed)


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from Adafruit IO!")


#def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    #print(f"New message on topic {topic}: {message}")


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

# If you need to use certificate/key pair authentication (e.g. X.509), you can load them in the
# ssl context by uncommenting the lines below and adding the following keys to the "secrets"
# dictionary in your secrets.py file:
# "device_cert_path" - Path to the Device Certificate
# "device_key_path" - Path to the RSA Private Key
# ssl_context.load_cert_chain(
#     certfile=secrets["device_cert_path"], keyfile=secrets["device_key_path"]
# )

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=1883,
    username=aio_username,
    password=aio_key,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
#mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to Adafruit IO...")
mqtt_client.connect()

Humidity_val = 0
Temperature_val = 0
CO2_val = 0
while True:
    # Poll the message queue
    mqtt_client.loop()
    with busio.I2C(SCL, SDA) as i2c:
        sht = adafruit_sht4x.SHT4x(i2c)
        Humidity_val = sht.relative_humidity
        Temperature_val = sht.temperature
    with busio.I2C(SCL, SDA, frequency=50000) as i2c:
        scd = adafruit_scd30.SCD30(i2c)
        data = scd.data_available
        if data:
            CO2_val = scd.CO2
            # Send a new message
            print(f"Sending Humidity value: {Humidity_val}...")
            mqtt_client.publish(humidity_feed, Humidity_val)
            print(f"Sending Temperature value: {Temperature_val}...")
            mqtt_client.publish(temperature_feed, Temperature_val)
            print(f"Sending CO2 value: {CO2_val}...")
            mqtt_client.publish(co2_feed, CO2_val)
            print("Sent!")
            time.sleep(30)