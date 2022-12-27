import ubinascii
import machine

# LINE secrets
LINE_ACCESS_TOKEN = ""
LINE_GROUP_ID = ""

# WIFI
WIFI_SSID = ""
WIFI_PASSWORD = ""

# BROKER
BROKER_HOST = ""
BROKER_PORT = 1883
BROKER_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
BROKER_TOPIC_SUB = b""
BROKER_TOPIC_PUB = b""
