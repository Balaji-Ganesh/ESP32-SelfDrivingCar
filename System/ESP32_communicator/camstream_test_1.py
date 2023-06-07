import websockets
import asyncio
import base64
import urllib.request
import numpy as np
import cv2

async def listen():
    url = "ws://192.168.81.165:81"

    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            # print("Received message", msg)
            npimg = np.array(bytearray(msg), dtype=np.uint8) # even try with msg.data
            print(npimg)
            img = cv2.imdecode(npimg, -1)
            cv2.imshow("img", img)
            cv2.waitKey(1)
            # decoded = base64.b64decode(msg, validate=False)
            # print("decoded msg: ", decoded)

            # response = urllib.request.urlopen(msg)
            # print(response)
            # # print(type(msg))  # getting as 'byte' type -- indicates "binary data"
            # print(base64.b32decode(msg))

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


"""