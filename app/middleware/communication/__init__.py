"""
This file prepares the required setup for the processing.
This
    - establishes bi-directional communication between ESP32 and system and
        exposes those websockets -- for use in other files.
    - get the processed camera feed and display in web-app
    
"""
import websockets

"""***************************** Initial configurations *****************************"""
esp32_ip = '172.168.1.132'                          # set it to the assigned IP address to ESP32 when connected to WiFi.
camera_port, data_port = 81, 82                     # configured ports for camera and data-transfer in ESP32.
camera_ws_url = "ws://"+esp32_ip+":"+str(camera_port)    # url of camera websockets
data_txrx_url = "ws://"+esp32_ip+":"+str(data_port)      # url of data transfer websockets
# FIXME: make the way of setting the IP and ports -  dynamically. Say by use of environment variables.

#### Establish websocket communications...
camera_ws = websockets.connect(camera_ws_url)
data_ws = websockets.connect(data_txrx_url)

# Expose functionalities of this module to other modules...
from .esp32_communicator import get_cam_feed
from .web_communicator import *