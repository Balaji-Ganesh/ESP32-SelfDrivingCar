"""
This file uses established websocket communication between ESP32 and the system for 
exchanging stream of messages.
"""
# Library imports
import cv2
import numpy as np
# Necessary local imports
from . import camera_ws as ws, data_ws, socketio   # import websockets for communication
import websockets


""" --------------- Utility functions ------------ """
# Camera related..
async def get_cam_feed():
    """This function with the established websocket, gets the cam feed form ESP32.
        
    Usage: Just call this function as like some generator in loop to get the feed.

    Yields:
        cv2 image: Frames sent by ESP32
    """
    print("[DEBUG] esp32: Proceeding to begin stream from ESP32....")
    try:
        print("[DEBUG] esp32: Stream begins from ESP32....")
        while True:
            msg = await ws.recv()
            print("[DEBUG] esp32: Received frame from esp32")
            npimg = np.array(bytearray(msg), dtype=np.uint8) # even try with msg.data
            # print(npimg)
            img = cv2.imdecode(npimg, -1)
            # send the image to web-app
            socketio.emit('img_data', img)
            cv2.imshow("img", img)
            if cv2.waitKey(1) == 27:
                print('EXITING')
                break
    except websockets.exceptions:
        print("[EXCEPTION] esp32: Receiving frames error. Connection might have broken, please try again. \nerror: ",e)
    except Exception as e:
        print("[EXCEPTION] esp32: error: ",e)
    finally:
        await ws.close()

