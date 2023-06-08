"""This script connects to the ESP32 server via websockets. Gets the camera feed and displays in a window"""
import websockets
import asyncio
import numpy as np
import cv2

url = "ws://172.168.1.132:81"

async def listen():

    async with websockets.connect(url) as ws:
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


asyncio.get_event_loop().run_until_complete(listen())

"""
src: https://youtu.be/tgtb9iucOts
conclusion:
    Like with the websockets-getting the data. There with the `msg` argument,
    But, still the question exists.. how to decode it.??

    another issue:
        there in the on_message() function, even though any print statements present at end after some functions -- they are never executed.
        -- is it because of synchronous connection?????????????

from docs: https://websockets.readthedocs.io/en/2.4/index.html?highlight=recv#websockets.protocol.WebSocketCommonProtocol.recv
    returns `str` for string, `byte` for binary frame
    - check what you are getting -->>>>>>>>>>>>> Getting <class 'bytes'> <<< means binary data.
    Now need to find the way to decode.

By GRACE... finally now working.
Possible from:
 - https://youtu.be/92UBFhPJQJ8?t=689 <<-- for decoding the image in python
 - http://www.iotsharing.com/2020/03/demo-48-using-websocket-for-camera-live.html <<-- for setting up streaming at ESP32.

 Now only thing pending is -- to establish communication from system to ESP32.
    
// sending data from System to ESP32.
    https://forum.arduino.cc/t/websocketserver-parsing-and-using-payload/631151 <<<<<<<<<------- at arduino side.
    https://websockets.readthedocs.io/en/stable/reference/asyncio/server.html#websockets.server.WebSocketServerProtocol.send <<<<<<---------- at system side
 
 """