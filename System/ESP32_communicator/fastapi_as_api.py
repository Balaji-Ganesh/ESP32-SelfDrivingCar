from fastapi import FastAPI
import asyncio
import websockets
import cv2
import numpy as np

app = FastAPI()

esp32_ip = '192.168.134.165'                          # set it to the assigned IP address to ESP32 when connected to WiFi.
camera_port, data_port = 81, 82                     # configured ports for camera and data-transfer in ESP32.
camera_ws_url = "ws://"+esp32_ip+":"+str(camera_port)    # url of camera websockets
data_txrx_url = "ws://"+esp32_ip+":"+str(data_port)      # url of data transfer websockets

cam_ws, data_ws = None, None
async def establish_line():
    global cam_ws, data_ws
    try:
        cam_ws = await websockets.connect(camera_ws_url)
        data_ws = await websockets.connect(data_txrx_url)
        print("Communication line established")
        return 'Line established'
    except Exception as e:
        print("[EXCEPTION] Couldn't establish line. Error: ", e)
        return 'Error in establishing line'

async def camera_client():
    print("------------------------------------------- Getting camera feed")
    try:
        cam_ws = await websockets.connect(camera_ws_url)
        print("Connection established")
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
        print("[EXCEPTION] Camera streaming interrupted")
    return 'ERROR in fetching feed'
        
async def collision_dist_client():
    print("------------------------------------------- Getting ultra-sonic feed")
    data_ws = await websockets.connect(data_txrx_url)
    while True:
        msg = await data_ws.recv()
        print("collsion distance: ", msg)
    
@app.get('/establish-line')
async def establish():
    task = asyncio.create_task(establish_line())
    return await task

@app.get('/camera-feed/')
async def get_camera_feed():
    try:
        task = asyncio.create_task(camera_client())
        return await task
    except KeyboardInterrupt:
        return 'Camera data fetching interrupted'

@app.get('/collision-distance')
async def get_collision_distance():
    try:
        print("-----------------check:  ", data_ws)
        task = asyncio.create_task(collision_dist_client())
        return await task
    except KeyboardInterrupt:
        return 'Collsion data fetching interrupted'