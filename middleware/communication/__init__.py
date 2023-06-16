# This file is from the branch `experiments` as `fastapi_as_api_in_class.py`
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
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

        self.cam_ws = None
        self.data_ws = None

        self.task = None
        self.router = APIRouter()

        @self.router.get("/")
        async def read_root():
            return {"Hello": "World"}

        @self.router.get("/connection/{function:str}")
        async def connections_handler(function: str):
            if function == 'establish':
                if self.cam_ws is None and self.data_ws is None:
                    task = asyncio.create_task(
                        esp32._connection_establisher(self))
                    success = await task
                    return {"message": "Connection to ESP32 established."} if success else {"message": "Failure in ESP32 connection establishment. Please check log."}
                else:
                    return {"message": "Connections already established."}
            elif function == 'terminate':
                if self.cam_ws is not None and self.data_ws is not None:
                    task = asyncio.create_task(
                        esp32._connection_terminater(self))
                    success = await task
                    return {"message": "ES32 connections terminated successfully.."} if success else {"message": "Failure in termination of ESP32 connections. Please check log."}
                else:
                    return {"message": "Connections already terminated."}
            else:
                return {'error': 'Invalid function invoked.'}

        @self.router.get("/camera-feed/{function:str}")
        async def camera_feed_handler(function: str):
            if function == 'start':
                # check connection status..
                if self.cam_ws is None:
                    return {'error': 'No connection established with ESP32. Please establish first.'}
                # when connection already established..
                if self.cam_task is None:
                    self.cam_task = asyncio.create_task(
                        esp32._camera_client(self))
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
                    # FIXME: The below one, is for testing purposes. Remove once done.
                    cv2.destroyAllWindows()
                    return {"message": "Camera task stopped."}
                else:
                    return {"message": "No camera task is currently running."}
            else:
                return {'error': 'Invalid function invoked.'}

        @self.router.get("/collision-distance/{function}")
        async def collision_dist_handler(function: str):
            if function == 'start':
                # check connection status..
                if self.data_ws is None:
                    return {'error': 'No connection established with ESP32. Please establish first.'}
                # when connection already established..
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
            else:
                return {'error': 'Invalid function invoked.'}


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


class WebManager:
    """Manages all the connections to the web-app.
    """

    def __init__(self):
        self.router = APIRouter()

        @self.router.get('/web')
        def sayhello():
            return 'Hello Web app'

        @self.router.websocket("/web/text")
        async def websocket_endpoint(websocket: WebSocket):
            await manager.connect(websocket)

            try:
                while True:
                    # data = await websocket.receive_text()
                    await manager.send_personal_message("You wrote: Hello Rama..!!", websocket)
                    # await manager.broadcast("Client #123 says: How are you Rama?")
            except WebSocketDisconnect:
                manager.disconnect(websocket)
                await manager.broadcast("Client #123 left the chat")
