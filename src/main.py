# main.py

import urequests as requests
from boot import (
    lcd,
    ir,
    builtin_led,
    do_connect,
    restart_and_reconnect,
    connect_and_subscribe,
)
from config import (
    BROKER_TOPIC_PUB,
    BROKER_TOPIC_SUB,
    LINE_ACCESS_TOKEN,
    LINE_GROUP_ID,
    WIFI_PASSWORD,
    WIFI_SSID,
    BROKER_CLIENT_ID,
    BROKER_HOST,
    BROKER_PORT,
)
from machine import sleep


def send_message():
    ENDPOINT = "https://api.line.me/v2/bot/message/push"

    HEADERS = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    }

    BODY = {
        "to": LINE_GROUP_ID,
        "messages": [
            {"type": "text", "text": "You have a guest waiting for you at the door."}
        ],
    }

    res = requests.post(url=ENDPOINT, json=BODY, headers=HEADERS)
    if res.status_code == 200:
        print("Successfully send notification")
    else:
        print(res.text)


def action():
    print("Visitor detected")
    send_message()
    client.publish(BROKER_TOPIC_PUB, b"visitor count=1")


def on_message_callback(topic, msg):
    print(f"[{topic.decode()}] MQTT client received message: {msg.decode()}")
    lcd.clear()
    lcd.putstr(msg.decode())


# Execution start from here

# IR sensor config
REQUIRED_DETECTION_TIME = 3  # in seconds
HARD_LIMIT_TIME = REQUIRED_DETECTION_TIME * 10 + 5

# Helper variable
counter = 0
right_to_send = True

builtin_led.value(1)

lcd.clear()
do_connect(WIFI_SSID, WIFI_PASSWORD)
try:
    client = connect_and_subscribe(
        hostname=BROKER_HOST, port=BROKER_PORT, client_id=BROKER_CLIENT_ID
    )
except OSError as e:
    restart_and_reconnect()

client.set_callback(on_message_callback)
client.subscribe(BROKER_TOPIC_SUB)
print(f"MQTT client subscribing to {BROKER_TOPIC_SUB.decode()}")

failed_fetch_counter = 0
while True:
    sleep(100)
    try:
        client.check_msg()
    except:
        if failed_fetch_counter >= 50:
            restart_and_reconnect()
        failed_fetch_counter += 1
        print("Cannot fetch message from broker")

    if ir.value() == 1:
        counter = HARD_LIMIT_TIME if counter >= HARD_LIMIT_TIME else counter + 1
    else:
        counter = 0 if counter < 0 else counter - 1

    if right_to_send and counter >= REQUIRED_DETECTION_TIME * 10:
        right_to_send = False
        builtin_led.value(0)
        action()

    if not right_to_send and counter <= 15:
        builtin_led.value(1)
        right_to_send = True
        print("Ready to send another notification")
