# This file is from the branch `experiments` as `fastapi_as_api_in_class.py`
import asyncio
from fastapi import FastAPI, APIRouter
import cv2

# Get the helpers..
from . import esp32

class ESP32Manager:
    """Manages all the communication related to the ESP32.
    """
    def __init__(self, esp32IP: str, cam_port: int = 81, data_port: int = 82):
        # set it to the assigned IP address to ESP32 when connected to WiFi.
        esp32_ip: str = esp32IP
        camera_port: int = cam_port
        # configured ports for camera and data-transfer in ESP32.
        data_port: int = data_port
        self.camera_ws_url: str = "ws://"+esp32_ip+":" + \
            str(camera_port)    # url of camera websockets
        self.data_txrx_url: str = "ws://"+esp32_ip+":" + \
            str(data_port)      # url of data transfer websockets

        self.cam_task = None
        self.data_task = None

        self.task = None
        self.router = APIRouter()

        @self.router.get("/")
        async def read_root():
            return {"Hello": "World"}
        
        @self.router.get("/camera-feed/{function}")
        async def camera_feed_handler(function: str):
            if function == 'start':
                if self.cam_task is None:
                    self.cam_task = asyncio.create_task(esp32._camera_client(self))
                    return {"message": "Camera task started."}
                else:
                    return {"message": "Camera task is already running."}
            elif function == 'stop':
                if self.cam_task is not None:
                    self.cam_task.cancel()
                    try:
                        await self.cam_task
                    except asyncio.CancelledError:
                        pass
                    self.cam_task = None
                    #FIXME: The below one, is for testing purposes. Remove once done.
                    cv2.destroyAllWindows()
                    return {"message": "Camera task stopped."}
                else:
                    return {"message": "No camera task is currently running."}

        @self.router.get("/collision-distance/{function}")
        async def collision_dist_handler(function: str):
            if function == 'start':
                if self.data_task is None:
                    self.data_task = asyncio.create_task(
                        esp32._collision_dist_fetcher(self))
                    return {"message": "Collision-data task started."}
                else:
                    return {"message": "Collision-data task is already running."}
            elif function == 'stop':
                if self.data_task is not None:
                    self.data_task.cancel()
                    try:
                        await self.data_task
                    except asyncio.CancelledError:
                        pass
                    self.data_task = None
                    return {"message": "Collision-data task stopped."}
                else:
                    return {"message": "No collision-data task is currently running."}
        
       
class WebManager:
    """Manages all the connections to the web-app.
    """
    def __init__(self):
        self.router = APIRouter()

        @self.router.get('/web')
        def sayhello():
            return 'Hello Web app'
