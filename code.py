import alarm
import board
import time
import digitalio
import neopixel
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_seesaw.seesaw import Seesaw
from digitalio import DigitalInOut, Direction, Pull

switch = DigitalInOut(board.D19)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# import secrets to initalize sensitive services
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])

# create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    port=secrets["mqtt_port"],
    username=secrets["mqtt_username"],
    password=secrets["mqtt_password"],
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()

while True:
    MQTT_TOPIC = "node_01/beam"
    beam = True
    if switch.value:
        beam = False
    print(beam)
    print("Publishing to %s" % MQTT_TOPIC)
    # mqtt_client.publish("node_01/moisture", soil_moisture)
    # mqtt_client.publish("node_01/temp", soil_temp)
    mqtt_client.publish("node_01/beam", str(beam))
    
    time.sleep(2)

    

