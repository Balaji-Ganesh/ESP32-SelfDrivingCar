"""
This file prepares the required setup for the processing.
This
    - establishes bi-directional communication between ESP32 and system and
        exposes those websockets -- for use in other files.
    - get the processed camera feed and display in web-app
    
"""
import websockets
import asyncio

"""***************************** Initial configurations *****************************"""
esp32_ip = '192.168.119.165'                          # set it to the assigned IP address to ESP32 when connected to WiFi.
camera_port, data_port = 81, 82                     # configured ports for camera and data-transfer in ESP32.
camera_ws_url = "ws://"+esp32_ip+":"+str(camera_port)    # url of camera websockets
data_txrx_url = "ws://"+esp32_ip+":"+str(data_port)      # url of data transfer websockets
# FIXME: make the way of setting the IP and ports -  dynamically. Say by use of environment variables.

#### Establish websocket communications...
async def establish_connection():
    global camera_ws, data_ws   # defining as global, as to be used in other file
    camera_ws = await websockets.connect(camera_ws_url)
    data_ws = await websockets.connect(data_txrx_url)
    print("Connection to ESP32 established successfully..!!")

asyncio.get_event_loop().run_until_complete(establish_connection())

# Expose functionalities of this module to other modules...
from .esp32_communicator import get_cam_feed
from .web_communicator import *