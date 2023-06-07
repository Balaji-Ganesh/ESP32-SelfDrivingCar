import websockets
import asyncio
import base64
import urllib.request

async def listen():
    url = "ws://192.168.4.1/Camera"

    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            # print(type(msg))  # getting as 'byte' type -- indicates "binary data"
            print(base64.b32decode(msg))

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