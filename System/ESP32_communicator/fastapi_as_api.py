from fastapi import FastAPI
import asyncio
import websockets

app = FastAPI()

url = 'ws://192.168.157.165:82'

@app.get('/collision-distance')
async def listen():
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            print("collsion distance: ", msg)
