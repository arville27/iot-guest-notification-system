# main.py

import urequests as requests
from boot import client
from config import BROKER_TOPIC_PUB, BROKER_TOPIC_SUB, LINE_ACCESS_TOKEN, LINE_GROUP_ID
from lib.i2c_lcd import I2cLcd
from machine import sleep, Pin, I2C

# I2C LCD display config
I2C_ADDR = 0x27
TOTAL_ROWS = 4
TOTAL_COLUMNS = 20

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)  # initializing the I2C method for ESP8266
lcd = I2cLcd(i2c, I2C_ADDR, TOTAL_ROWS, TOTAL_COLUMNS)
ir = Pin(13, Pin.IN)  # D7 (E18-D80NK, blue-GND, brown-VCC, black-OUT)
builtin_led = Pin(2, Pin.OUT)  # D4 (built in LED)

# IR sensor config
REQUIRED_DETECTION_TIME = 3  # in seconds
HARD_LIMIT_TIME = REQUIRED_DETECTION_TIME * 10 + 5

# Helper variable
counter = 0
right_to_send = True

builtin_led.value(1)


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


client.set_callback(on_message_callback)
client.subscribe(BROKER_TOPIC_SUB)
print(f"MQTT client subscribing to {BROKER_TOPIC_SUB.decode()}")

while True:
    sleep(100)
    client.check_msg()
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
