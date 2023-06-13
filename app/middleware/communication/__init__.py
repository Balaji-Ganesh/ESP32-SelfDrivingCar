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
import logging
from flask_socketio import SocketIO



class ESP32Communication:
    async def _establish_esp32connection(self):
        global camera_ws, data_ws   # defining as global, as to be used in other file
        try:
            self.camera_ws = await websockets.connect(self.camera_ws_url)
            self.data_ws = await websockets.connect(self.data_txrx_url)
            logging.debug(
                "comm: Connection to ESP32 established successfully..!!")
        except websockets.exceptions.ConnectionClosedError:
            logging.error(
                "comm: Cannot connect to ESP32. Try the following solutions..")
            logging.error(
                "comm: Please ensure that ESP32 is powered on. IP address (of same network) of ESP32 is properly entered.")
        except Exception as e:
            logging.error("comm: error: ", e)

    def init_communication(self, ip: str, cam_port: int = 81, data_port: int = 82):
        # set it to the assigned IP address to ESP32 when connected to WiFi.
        self.esp32_ip = ip
        # configured ports for camera and data-transfer in ESP32.
        self.camera_port, self.data_port = cam_port, data_port
        self.camera_ws_url = "ws://"+self.esp32_ip+":" + \
            str(self.camera_port)    # url of camera websockets
        # url of data transfer websockets
        self.data_txrx_url = "ws://"+self.esp32_ip+":"+str(self.data_port)
        # FIXME: make the way of setting the IP and ports -  dynamically. Say by use of environment variables.
        logging.debug('ESP32 communication setup done')

        logging.debug(
            f'Proceeding to establish communication with IP: {self.esp32_ip} and ports {self.camera_port}, {self.data_port}')
        asyncio.get_event_loop().run_until_complete(self._establish_esp32connection())

    # import other utility modules
    from .esp32_communicator import get_cam_feed


class WebCommunication:
    # Import socketio event handlers
    from .web_communicator import handle_connect, handle_disconnect, handle_ack, handle_stream

    def init_communication(self, socketio):
        self.sock: SocketIO = socketio

        # register event handlers..
        # socketio.on_event('event', handler=handle_manual_mode, namespace='/') - alternative for @socketio.on('event)
        self.sock.on_event('connect', self.handle_connect)
        self.sock.on_event('disconnect', self.handle_disconnect)
        self.sock.on_event('ack', self.handle_ack)
        self.sock.on_event('stream', self.handle_stream)

# Defining globally to enable accessiblity to other modules.
web_comm = WebCommunication()
esp32_comm = ESP32Communication()
