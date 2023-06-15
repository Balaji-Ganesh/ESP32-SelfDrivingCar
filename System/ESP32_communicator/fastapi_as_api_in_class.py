import asyncio
from fastapi import FastAPI, APIRouter
import websockets

import cv2
import numpy as np
import logging

class ESP32Manager:
    def __init__(self, esp32IP:str, cam_port:int=81, data_port:int=82):
        
        esp32_ip:str = esp32IP                       # set it to the assigned IP address to ESP32 when connected to WiFi.
        camera_port:int = cam_port
        data_port:int = data_port                     # configured ports for camera and data-transfer in ESP32.
        self.camera_ws_url:str = "ws://"+esp32_ip+":"+str(camera_port)    # url of camera websockets
        self.data_txrx_url:str = "ws://"+esp32_ip+":"+str(data_port)      # url of data transfer websockets

        self.cam_task = None
        self.data_task = None

        self.task = None
        self.router = APIRouter()

        @self.router.get("/")
        async def read_root():
            return {"Hello": "World"}
        
        @self.router.get("/camera-feed/{function}")
        async def camera_feed_handler(function:str):
            if function == 'start':
                if self.cam_task is None:
                    self.cam_task = asyncio.create_task(self._camera_client())
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
                    cv2.destroyAllWindows()
                    return {"message": "Camera task stopped."}
                else:
                    return {"message": "No camera task is currently running."}

        @self.router.get("/collision-distance/{function}")
        async def collision_dist_handler(function:str):
            if function == 'start':
                if self.data_task is None:
                    self.data_task = asyncio.create_task(self._collision_dist_fetcher())
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
        
    async def _camera_client(self):
        try:
            cam_ws = await websockets.connect(self.camera_ws_url)
            while True:
                msg = await cam_ws.recv()
                npimg = np.array(bytearray(msg), dtype=np.uint8) # even try with msg.data
                img = cv2.imdecode(npimg, -1)
                cv2.imshow("img", img)
                if cv2.waitKey(1) == 27:
                    print('EXITING')
                    cv2.destroyAllWindows()
                    return 'Camera feed stopped by user'
        except Exception as e:
            logging.error("[EXCEPTION] Camera streaming interrupted. Error: ", e)
        finally:
            await cam_ws.close()
            logging.debug("Camera Websockets Connection closed successfully")
        return 'ERROR in fetching feed'
    
    async def _collision_dist_fetcher(self):
        async with websockets.connect(self.data_txrx_url) as websocket:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")

                # Process the message or perform any other task logic

                # response = f"Processed: {message}"
                # await websocket.send(response)
                # print(f"Sent response: {response}")


app = FastAPI()
obj = ESP32Manager(esp32IP='192.168.134.165' )

app.include_router(obj.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.2", port=8000, reload=True)
# modified version of chatGPT's help.