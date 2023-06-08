""" This script is a modification of `asynchronous_streaming.py`.
    This will connect to ESP32 server via websockets and
      - gets the ultrasonic collision distance feed.
      - sends the navigation controls
"""

import websockets
import asyncio

url = "ws://172.168.1.132:82"

async def listen():
    navigation_data = {
      "s": 256,
      "d": "U", # 0: UP, 1: Down, 2:LEFT, 3: Right -- working even with the string. But going to adopt the integer format.
      "i": 40
    }

    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            print("collsion distance: ", msg)

            # send navigation controls to the ESP32
            await ws.send(str(navigation_data))

asyncio.get_event_loop().run_until_complete(listen())