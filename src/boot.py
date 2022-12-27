# boot.py - - runs on boot-up

from machine import sleep
import machine
from config import (
    WIFI_SSID,
    WIFI_PASSWORD,
    BROKER_CLIENT_ID,
    BROKER_HOST,
    BROKER_PORT,
)


def do_connect():
    import network

    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Connecting to network", end="")
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            sleep(1000)
            print(".", end="")
            pass
        print()
    print("Connected:", wlan.ifconfig())


def connect_and_subscribe():
    from umqtt.simple import MQTTClient

    client = MQTTClient(BROKER_CLIENT_ID, BROKER_HOST, BROKER_PORT)
    client.connect()
    print(f"Connected to {BROKER_HOST} MQTT broker")
    return client


def restart_and_reconnect():
    print("Failed to connect to MQTT broker. Reconnecting...")
    sleep(1000)
    machine.reset()


do_connect()
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()
