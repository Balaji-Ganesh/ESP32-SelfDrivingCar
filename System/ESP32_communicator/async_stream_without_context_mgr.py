"""
This file is modification of `asynchronouse_streaming.py` with a change as
- Stream without using context manager (~not using `with` operator which handles opening and closing)

1st test:
    - test without using context manager - as per the ref. below.
2nd test:
    - initiate the connection in another file and use that in this file.
    - this is done by using another file called `connection_initiator.py`
"""
import websockets
import asyncio
import numpy as np
import cv2
from connection_initiator import ws

# url = "ws://192.168.64.165:81"
async def listen():
    # ws = await websockets.connect(url)
    try:
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
    except Exception as e:
        print(e)
    finally:
        await ws.ws_client.close()


asyncio.get_event_loop().run_until_complete(listen())

# Reference: https://stackoverflow.com/questions/64897045/how-to-connect-to-websocket-without-context-manager