"""
This file prepares the required setup for the processing.
This
    - establishes bi-directional communication between ESP32 and system and
        exposes those websockets -- for use in other files.
    - establish bi-directional communication with python and web-app and
        exposes that socket to use in other modules.
    
"""
import websockets
import asyncio
from flask_socketio import SocketIO
# from app import create_app
# from .web_communicator import *
# from .esp32_communicator import get_cam_feed

"""***************************** Initial configurations *****************************"""
esp32_ip = '192.168.0.165'                          # set it to the assigned IP address to ESP32 when connected to WiFi.
# configured ports for camera and data-transfer in ESP32.
camera_port, data_port = 81, 82
camera_ws_url = "ws://"+esp32_ip+":" + \
    str(camera_port)    # url of camera websockets
# url of data transfer websockets
data_txrx_url = "ws://"+esp32_ip+":"+str(data_port)
# FIXME: make the way of setting the IP and ports -  dynamically. Say by use of environment variables.

socketio = ""
"""***************************** Helper functions  *****************************"""
async def establish_esp32connection():
    global camera_ws, data_ws   # defining as global, as to be used in other file
    try:
        camera_ws = await websockets.connect(camera_ws_url)
        data_ws = await websockets.connect(data_txrx_url)
        print("[DEBUG] comm: Connection to ESP32 established successfully..!!")
    except websockets.exceptions.ConnectionClosedError:
        print("[EXCEPTION] comm: Cannot connect to ESP32. Try the following solutions..")
        print("[EXCEPTION] comm: Please ensure that ESP32 is powered on. IP address (of same network) of ESP32 is properly entered.")
    except Exception as e:
        print("[EXCEPTION] comm: error: ", e)


def establish_communications(webapp, sock):
    """  ----------   Establish socketio communication with web-app    ----------     """
    # global socketio
    # socketio: SocketIO = SocketIO()
    sock.init_app(webapp, cors_allowed_origins="*", logger=True, engineio_logger=True)
    socketio = sock
    # socketio = SocketIO(webapp, cors_allowed_origins="*")
    print("[DEBUG] comm: Python <--> Web-app connection established.")

    """  ----------   Establish websocket communication with esp32    ----------     """
    # if camera_ws is not None and data_ws is not None:
    asyncio.get_event_loop().run_until_complete(establish_esp32connection())
    print("[DEBUG] comm: Python <--> ESP32 communication established.")
    # else:
    #     print("[DEBUG] comm: Connection to ESP32 already established")



# Expose functionalities of this module to other modules...
# print("[DEBUG] Communication module speaking: About to import esp32 and web communicator modules")
# print("[DEBUG] Communication module speaking: Imported esp32 and web communicator modules")
