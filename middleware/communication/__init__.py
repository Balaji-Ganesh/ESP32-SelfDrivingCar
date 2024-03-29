# This file is from the branch `experiments` as `fastapi_as_api_in_class.py`
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2
from enum import Enum
from typing import Any
import socketio
import json
import websockets

class StatusManager(Enum):
    ESTABLISHED = 1  # to indicate - connection is established between two parties
    TERMINATED = 2  # to indicate - connection is terminated/not connected between two parties


class ESP32Manager():
    """Manages all the communication related to the ESP32.
    """
    # status maintainer -- to use in other modules
    conn_status = StatusManager.TERMINATED
    # websockets to use in another modules..
    cam_ws = None
    data_ws = None
    # Get the helpers..
    from .esp32 import camera_client, collision_dist_fetcher, connection_establisher, _connection_terminater  # make the

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

        @self.router.get("/connection/{function:str}")
        async def connections_handler(function: str):
            if function == 'establish':
                if ESP32Manager.cam_ws is None and ESP32Manager.data_ws is None:
                    task = asyncio.create_task(
                        self.connection_establisher())
                    success = await task
                    return {"message": "Connection to ESP32 established."} if success else {"message": "Failure in ESP32 connection establishment. Please check log."}
                else:
                    return {"message": "Connections already established."}
            elif function == 'terminate':
                if ESP32Manager.cam_ws is not None and ESP32Manager.data_ws is not None:
                    task = asyncio.create_task(
                        self._connection_terminater())
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
                if ESP32Manager.cam_ws is None:
                    return {'error': 'No connection established with ESP32. Please establish first.'}
                # when connection already established..
                if self.cam_task is None:
                    self.cam_task = asyncio.create_task(
                        self.camera_client())
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
                if ESP32Manager.data_ws is None:
                    return {'error': 'No connection established with ESP32. Please establish first.'}
                # when connection already established..
                if self.data_task is None:
                    self.data_task = asyncio.create_task(
                        self.collision_dist_fetcher())
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
    # FIXME: Later if could work even withoug this class, remove this.
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_data(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_response(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def send_bin(self, message: str, websocket: WebSocket):
        await websocket.send_bytes(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class WebManager():
    """Manages all the connections to the web-app.
    """
    conn_status = StatusManager.TERMINATED

    # Get the helpers
    from .web import send_collision_data, stream_camera_feed

    def __init__(self):
        self.sio: Any = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=['http://127.0.0.2:5000', 'ws://127.0.0.2:5000'])
        self.socket_app = socketio.ASGIApp(socketio_server=self.sio, socketio_path='foo')
        self.router = APIRouter()

        # To handle start and stop of features..
        self.collision_task = None
        self.camera_task = None

        # to hold of speed and interval
        self.speed=150
        self.interval=52

        @self.router.get('/web')
        def sayhello():
            return 'Hello Web app' 

        # -------------------------------------------- Defining socketio event handlers... -----------------------------
        @self.sio.on('connect')
        async def handle_connect(sid, env):
            print(f"client-{sid} connected.")
            await self.sio.emit('ack', 'You are now connected to server')

        @self.sio.on('disconnect')
        async def handle_disconnect(sid):
            print(f"client-{sid} disconnected.")
            #FIXME: Here remove all the tasks if pending..
            
        @self.sio.on('ack')
        async def handle_ack(sid, msg):
            print(f"client-{sid} acknowledges: {msg}.")
        
        @self.sio.on('json')
        async def handle_json(sid, msg):
            print(f"client-{sid} sends: {msg}.")

        ### -------------------------------------- Handlers, specifically to listen regarding sppecific features.
                
        @self.sio.on('collision_feed')
        async def handle_collision_feed(sid, request):
            print(f"client-{sid} on collision: {request}.")
            # take the action accordingly..
            if request == 'start':
                if self.collision_task is None:
                    self.collision_task = asyncio.create_task(self.send_collision_data())
                    await self.sio.send(json.dumps({'info': 'Server started sending collision feed.'}))
                else:
                    await self.sio.send(json.dumps({'error': 'Server already in sending collision feed.'}))
            elif request == 'stop':
                if self.collision_task is not None:
                    self.collision_task.cancel()
                    try:
                        await self.collision_task
                    except asyncio.CancelledError:
                        pass
                    self.collision_task = None  # set to empty, to use next time freshly
                    await self.sio.send(json.dumps({'info': 'Server stopped sending collision feed.'}))
                else:
                    await self.sio.send(json.dumps({'error': 'Server already stopped collision feed.'}))
            else:
                await self.sio.send(json.dumps({'error': 'collsion_feed - sent invalid request'}))
        
        @self.sio.on('camera_feed')
        async def handle_camera_feed(sid, request):
            
            print(f"client-{sid} on camera: {request}.")
            # take the action accordingly..
            if request == 'start':
                if self.camera_task is None:
                    self.camera_task = asyncio.create_task(self.stream_camera_feed())
                    await self.sio.send(json.dumps({'info': 'Server started stream ESP32 camera feed.'}))
                else:
                    await self.sio.send(json.dumps({'error': 'Server already in streaming ESP32 camera feed.'}))
            elif request == 'stop':
                if self.camera_task is not None:
                    self.camera_task.cancel()
                    try:
                        await self.camera_task
                    except asyncio.CancelledError:
                        pass
                    self.camera_task = None  # set to empty, to use next time freshly
                    await self.sio.send(json.dumps({'info': 'Server stopped streaming ESP32 camera feed.'}))
                else:
                    await self.sio.send(json.dumps({'error': 'Server already streaming ESP32 camera feed.'}))
            else:
                await self.sio.send(json.dumps({'error': 'collsion_feed - sent invalid request'}))

        @self.sio.on('navigations')
        async def handle_navigations(sid, request):
            print(f"client-{sid} on navigations: {request}.")
            from main import esp32_mngr

            if request == 'start':
                await self.sio.send(json.dumps({'info': 'Server ready to take navigations.'}))
                print("status: connection establishment: ", esp32_mngr.conn_status)
                print("status: websocket status: ", ESP32Manager.data_ws)
            elif request == 'stop':
                await self.sio.send(json.dumps({'info': 'Server stopps to take navigations.'}))
        
        @self.sio.on('direction')
        async def handle_direction(sid, dir):
            print(f"client-{sid} on direction: {dir}.")
            from main import esp32_mngr
            print("status: connection establishment")
            try:
                if esp32_mngr.conn_status == StatusManager.ESTABLISHED:
                    if ESP32Manager.data_ws is not None:
                        payload = 'direction'+','+dir # Arrange in the format, that ESP32 can understand.
                        await ESP32Manager.data_ws.send(str(payload))
                else:
                    print("couldn't able send data to ESP32")
            # handle connection close..
            except websockets.exceptions.ConnectionClosedError as e:
                print("Oops..!! Connection closed. Auto-Reconnecting... Please wait..")
                # try reconnecting.. first terminate explicitly ( to avoid multiple connection instances )
                task = asyncio.create_task(esp32_mngr._connection_terminater())
                success = await task
                if success: 
                    print("Connection cleaned up.!! Establishing fresh connection, please wait..!!")
                    task = asyncio.create_task(esp32_mngr.connection_establisher())
                    success = await task
                    if success:
                        print("Connection re-established..!!")
                else:
                    print("auto-reconnect failed. Please try manually.")
            # to handle other exceptions..
            except Exception as e:
                print("[EXCEPTION] exception occured: ", e)
                
        # @self.sio.on("broadcast")
        # async def broadcast(sid, msg):
        #     print(f"broadcast {msg}")
        #     await self.sio.emit("event_name", msg)  # or send to everyone