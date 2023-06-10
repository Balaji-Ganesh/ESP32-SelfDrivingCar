"""
This file is created as a part of 2nd test in `async_stream_without_context_mgr.py`
"""
import websockets
import asyncio

url = "ws://192.168.64.165:81"
async def listen():
    global ws
    ws = await websockets.connect(url)
    

asyncio.get_event_loop().run_until_complete(listen())
