# boot.py - - runs on boot-up

from machine import Pin, sleep, I2C
from lib.i2c_lcd import I2cLcd
import machine
from config import (
    WIFI_SSID,
    WIFI_PASSWORD,
    BROKER_CLIENT_ID,
    BROKER_HOST,
    BROKER_PORT,
)

# I2C LCD display config
I2C_ADDR = 0x27
TOTAL_ROWS = 4
TOTAL_COLUMNS = 20

# GPIO Pin definition
# SCL = D1, SDA = D2
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)  # initializing the I2C method for ESP8266
lcd = I2cLcd(i2c, I2C_ADDR, TOTAL_ROWS, TOTAL_COLUMNS)


def do_connect(wifi_ssid: str, wifi_psk: str):
    import network

    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        lcd_message = f"Connecting to WIFI  SSID: {WIFI_SSID}"
        lcd.putstr(lcd_message)
        print("Connecting to network", end="")
        wlan.active(True)
        wlan.connect(wifi_ssid, wifi_psk)
        dot_counter = 0
        while not wlan.isconnected():
            sleep(1000)
            print(".", end="")
            if dot_counter == 3:
                lcd.clear()
                lcd.putstr(lcd_message)
                dot_counter = 0
            dot_counter += 1
            lcd.putchar(".")
            pass
        print()
    print("Connected:", wlan.ifconfig())
    lcd.clear()


def connect_and_subscribe(hostname: str, port: int, client_id: str):
    from umqtt.simple import MQTTClient

    client = MQTTClient(client_id, hostname, port)
    client.connect()
    print(f"Connected to {hostname} MQTT broker")
    return client


def restart_and_reconnect():
    print("Failed to connect to MQTT broker. Reconnecting...")
    sleep(1000)
    machine.reset()


lcd.clear()
do_connect(WIFI_SSID, WIFI_PASSWORD)
try:
    client = connect_and_subscribe(
        hostname=BROKER_HOST, port=BROKER_PORT, client_id=BROKER_CLIENT_ID
    )
except OSError as e:
    restart_and_reconnect()
