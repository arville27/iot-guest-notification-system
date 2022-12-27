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


def do_connect(wifi_ssid: str, wifi_psk: str):
    import network

    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Connecting to network", end="")
        wlan.active(True)
        wlan.connect(wifi_ssid, wifi_psk)
        while not wlan.isconnected():
            sleep(1000)
            print(".", end="")
            pass
        print()
    print("Connected:", wlan.ifconfig())


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


do_connect(WIFI_SSID, WIFI_PASSWORD)
try:
    client = connect_and_subscribe(
        hostname=BROKER_HOST, port=BROKER_PORT, client_id=BROKER_CLIENT_ID
    )
except OSError as e:
    restart_and_reconnect()
