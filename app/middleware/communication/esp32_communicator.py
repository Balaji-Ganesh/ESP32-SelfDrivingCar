"""
This file uses established websocket communication between ESP32 and the system for 
exchanging stream of messages.
"""
# Library imports
import cv2
import numpy as np
# Necessary local imports
from . import camera_ws, data_ws   # import websockets for communication

""" --------------- Utility functions ------------ """
# Camera related..
async def get_cam_feed():
    """This function with the established websocket, gets the cam feed form ESP32.
        
    Usage: Just call this function as like some generator in loop to get the feed.

    Yields:
        cv2 image: Frames sent by ESP32
    """
    async with camera_ws as ws:
        while True:
            msg = await ws.recv()
            # print("Received message", msg)
            npimg = np.array(bytearray(msg), dtype=np.uint8) # even try with msg.data
            # print(npimg)
            img = cv2.imdecode(npimg, -1)
            yield img   ## <<<<<<<<<<<<<<<<--- caller function gets the cam feed from here
            cv2.imshow("[DEBUG] ESP32 cam feed", img)
            if cv2.waitKey(1) == 27:
                print('EXITING')
                break

