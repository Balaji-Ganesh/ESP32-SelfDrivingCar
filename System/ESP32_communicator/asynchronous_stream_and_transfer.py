"""
    This script is a merge of two files `asynchronous_streaming.py`  and `asynchronous_transfer.py` .
    Why?
      For running both parallely.

"""
import websockets
import asyncio
import numpy as np
import cv2
from multiprocessing import Process

"""***************************** Initial configurations *****************************"""
esp32_ip = '172.168.1.132'                          # set it to the assigned IP address to ESP32 when connected to WiFi.
camera_port, data_port = 81, 82                     # configured ports for camera and data-transfer in ESP32.
camera_ws_url = "ws://"+esp32_ip+":"+str(camera_port)    # url of camera websockets
data_txrx_url = "ws://"+esp32_ip+":"+str(data_port)      # url of data transfer websockets

async def camera_client():
    async with websockets.connect(camera_ws_url) as ws:
        while True:
            msg = await ws.recv()
            # print("Received message", msg)
            npimg = np.array(bytearray(msg), dtype=np.uint8) # even try with msg.data
            # print(npimg)
            img = cv2.imdecode(npimg, -1)
            cv2.imshow("img", img)
            if cv2.waitKey(1) == 27:
                print('EXITING')
                break

async def data_transfer_client():
    # dummy data for now. Later will be sent dynamically from UI.
    navigation_data = {
      "s": 256,
      "d": "U", # 0: UP, 1: Down, 2:LEFT, 3: Right -- working even with the string. But going to adopt the integer format.
      "i": 40
    }

    async with websockets.connect(data_txrx_url) as ws:
        while True:
            msg = await ws.recv()
            print("collsion distance: ", msg)

            # send navigation controls to the ESP32
            await ws.send(str(navigation_data))

def stream_cam():
    asyncio.get_event_loop().run_until_complete(camera_client())

def transfer_data():
    asyncio.get_event_loop().run_until_complete(data_transfer_client())

if __name__ == '__main__':
    # Initiate multiprocessing..
    camProcess = Process(target=stream_cam)
    dataProcess = Process(target=transfer_data)
    
    # Start multiprocessing..
    camProcess.start()
    dataProcess.start()

    # Give instruction to not to exit until main quits.
    camProcess.join()
    dataProcess.join()


"""
References:
    - [Which to choose - Multithreading or Multiprocesssing?](https://www.geeksforgeeks.org/difference-between-multithreading-vs-multiprocessing-in-python/)
"""