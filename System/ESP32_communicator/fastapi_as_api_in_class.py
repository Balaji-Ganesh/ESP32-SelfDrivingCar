from fastapi import Depends, FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

import websockets
import cv2
import numpy as np
import asyncio
import logging

app = FastAPI()
router = InferringRouter()  # Step 1: Create a router

@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class Foo:
    # Attributes
    # Step 3: Add dependencies as class attributes
    def __init__(self):
        esp32_ip:str = '192.168.134.165'                       # set it to the assigned IP address to ESP32 when connected to WiFi.
        camera_port:int = 81
        data_port:int = 82                     # configured ports for camera and data-transfer in ESP32.
        self.camera_ws_url:str = "ws://"+esp32_ip+":"+str(camera_port)    # url of camera websockets
        self.data_txrx_url:str = "ws://"+esp32_ip+":"+str(data_port)      # url of data transfer websockets

        self.cam_ws: websockets.legacy.client.WebSocketClientProtocol
        self.data_ws: websockets.legacy.client.WebSocketClientProtocol


    # Helper functions
    async def _establish_line(self):
        try:
            self.cam_ws = await websockets.connect(self.camera_ws_url)
            self.data_ws = await websockets.connect(self.data_txrx_url)
            print("Communication line established. ", type(self.cam_ws))
            return 'Line established'
        except Exception as e:
            print("[EXCEPTION] Couldn't establish line. Error: ", e)
            return 'Error in establishing line'

    async def _camera_client(self):
        print("------------------------------------------- Getting camera feed")
        try:
            cam_ws = await websockets.connect(self.camera_ws_url)
            print("Connection established. Test: ", type(cam_ws))
            print("About to fetch frames")
            while True:
                msg = await cam_ws.recv()
                # print("Received message", msg)
                npimg = np.array(bytearray(msg), dtype=np.uint8) # even try with msg.data
                # print(npimg)
                img = cv2.imdecode(npimg, -1)
                cv2.imshow("img", img)
                if cv2.waitKey(1) == 27:
                    print('EXITING')
                    cv2.destroyAllWindows()
                    return '--- by from camerafeed'
        except Exception as e:
            logging.error("[EXCEPTION] Camera streaming interrupted. Error: ", e)
        finally:
            await cam_ws.close()
            logging.debug("Camera Websockets Connection closed successfully")
        return 'ERROR in fetching feed'
            
    async def _collision_dist_client(self):
        print("------------------------------------------- Getting ultra-sonic feed")
        try:
            data_ws = await websockets.connect(self.data_txrx_url)
            while True:
                msg = await data_ws.recv()
                print("collsion distance: ", msg)
        except Exception as e:
            logging.error("[_collision_dist_client] Error in fetching ultrasonic feed. Error: ",e)
            return 'Error in fetching collsion feed'
        finally:
            await data_ws.close()
            logging.debug("[_collision_dist_client] Camera Websockets Connection closed successfully")
        

    @router.get('/establish-line')
    async def establish(self):
        task = asyncio.create_task(self._establish_line())
        return await task

    @router.get('/camera-feed/')
    async def get_camera_feed(self):
        try:
            task = asyncio.create_task(self._camera_client())
            return await task
        except KeyboardInterrupt:
            return 'Camera data fetching interrupted'

    @router.get('/collision-distance')
    async def get_collision_distance(self):
        try:
            # print("-----------------check:  ", self.data_ws)
            task = asyncio.create_task(self._collision_dist_client())
            return await task
        except KeyboardInterrupt:
            return 'Collsion data fetching interrupted'

app.include_router(router)