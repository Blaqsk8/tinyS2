import alarm
import board
import time
import digialio
import neopixel
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_seesaw.seesaw import Seesaw

# MQTT Topic Setup
PUBLISH_DELAY = 60
MQTT_TOPIC = "state/moisture_node_01"
USE_DEEP_SLEEP = True

# moisture sensor setup
i2c_bus = board.I2C()
moisture_sensor = Seesaw(i2c_bus, addr=0x36)

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


    

