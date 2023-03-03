from neopixel import Neopixel
from time import sleep
from machine import pin
import network
import socket

# ---------------------------
# SETUP
# ---------------------------

# number of LEDs in the LED strip
NUM_LEDS = 5
# Maximum number of packets to hold in the buffer.
BUFFER_LEN = 1024
# Toggles FPS output (1 = print FPS over serial, 0 = disable output)
PRINT_FPS = 0
# Wifi Status LED
wifistatus_led = Pin("LED", Pin.OUT)

# ---------------------------
# CONSTANTS
# ---------------------------

# Output pin on the Raspberry Pi Pico
OUTPUT_PIN = 4
# WiFi Settings
WIFI_SSID = ""
WIFI_PASS = ""
wlan = network.WLAN(network.STA_IF)
# UDP Settings
UDP_PORT = 7777
UDP_SENDER_IP = ""

# ---------------------------
# FUNCTIONS
# ---------------------------

def WiFiConnect():
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
        wifistatus_led.on()
        print('network config:', wlan.ifconfig())
    
def WiFiDisconnect():
    print('disconnecting wifi')
    wlan.disconnect()
    wlan.active(False)
    wifistatus_led.off()
  
# ---------------------------
# MAIN
# ---------------------------

WifiConnect()
while True:
    while wlan.isconnected():
        
        UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPSocket.bind((wlan.ifconfig()[0], UDP_PORT))
        
        while True:
            data = UDPSocket.recvfrom(BUFFER_LEN)
            message = data[0]
            address = data[1]
            print(message)
        
    while not wlan.isconnected():
        wifistatus_led.off()
        WiFiConnect()
        
        
    
    
