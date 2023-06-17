"""
This file gets the processed output of the algorithm and sends it to the web-app.
"""
import asyncio
from threading import Thread
# Event handlers for socketio
import cv2
import base64
import json
import logging
import numpy as np

async def send_collision_data(self):
    logging.debug("came to send collision data")
    from main import esp32_mngr
    try:
        while True:
            logging.debug('Waiting for data...')
            dist = await esp32_mngr.data_ws.recv()
            logging.debug("Received collision data: "+ str(dist))
            await self.sio.emit('collsion_data', dist)
    except Exception as e:
        print('[EXCEPTION] An error occured in fetching collision data. Error: ', e)
        await self.sio.send(json.dumps({"error": "An error occured in fetching collision data from ESP32. \
                                        Make sure connection is established, and check logs."}))

async def stream_camera_feed(self):
    logging.debug("came to stream camera data")
    from main import esp32_mngr
    i=0.1
    try:
        while True:
            logging.debug('Waiting for data...')
            data = await esp32_mngr.cam_ws.recv()
            npimg = np.array(bytearray(data), dtype=np.uint8)
            img = cv2.imdecode(npimg, -1)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame = base64.encodebytes(frame).decode("utf-8")
            await self.sio.emit('camera_data', frame)
    except Exception as e:
        print('[EXCEPTION] An error occured in fetching camera feed. Error: ', e)
        await self.sio.send(json.dumps({"error": "An error occured in fetching camera from ESP32. \
                                        Make sure connection is established, and check logs"}))
            
    
