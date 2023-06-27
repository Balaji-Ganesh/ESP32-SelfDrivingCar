import socketio
import asyncio
   
# Async client
sio = socketio.AsyncClient(logger=True, engineio_logger=True)

# Registering event handlers
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

# connect to the server
async def establish_conn():
    await sio.connect("ws://192.168.147.165:82")
    print("sid: ",sio.sid)
    # return sio.sid  # assigned socket-id by the server

## Other handlers
async def onkeypress(event):
    print(event.name)
    await sio.send(event.name)

async def transfer_data():
    while True:
        # Do-nothing loop. Just use to wait, until force-closed with ctrl+c
        data = input("Enter data to send (type 'END' to quit): ")
        if data != 'END':
            await sio.send(data=data)
            print("ACK: sent successfully.")
        else:
            break

if __name__ == '__main__':
    # Establish connection with the server..
    # task = asyncio.create_task(establish_conn())
    # asyncio.new_event_loop().run_until_complete(establish_conn())
    # task = asyncio.create_task(establish_conn())
    # await task
    # task = sio.start_background_task(establish_conn)
    asyncio.run(establish_conn())
    asyncio.run(transfer_data())
    
    
"""
Log on 18th June 2023 - Sunday.


[arjuna@kurukshetra ESP32_communicator]$ python socketio-async-send.py 
Attempting polling connection to http://192.168.147.165:82/socket.io/?transport=polling&EIO=3
Traceback (most recent call last):
  File "/run/media/arjuna/WorkAndWorkResources/Work/Projects/MajorProject/SelfDrivingCar/System/ESP32_communicator/socketio-async-send.py", line 48, in <module>
    asyncio.run(establish_conn())
  File "/usr/lib/python3.10/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/usr/lib/python3.10/asyncio/base_events.py", line 649, in run_until_complete
    return future.result()
  File "/run/media/arjuna/WorkAndWorkResources/Work/Projects/MajorProject/SelfDrivingCar/System/ESP32_communicator/socketio-async-send.py", line 22, in establish_conn
    await sio.connect("ws://192.168.147.165:82")
  File "/home/arjuna/.local/lib/python3.10/site-packages/socketio/asyncio_client.py", line 109, in connect
    await self.eio.connect(url, headers=headers,
  File "/home/arjuna/.local/lib/python3.10/site-packages/engineio/asyncio_client.py", line 101, in connect
    return await getattr(self, '_connect_' + self.transports[0])(
  File "/home/arjuna/.local/lib/python3.10/site-packages/engineio/asyncio_client.py", line 214, in _connect_polling
    r.status), await r.json())
  File "/home/arjuna/.local/lib/python3.10/site-packages/aiohttp/client_reqrep.py", line 1104, in json
    raise ContentTypeError(
aiohttp.client_exceptions.ContentTypeError: 0, message='Attempt to decode JSON with unexpected mimetype: text/plain', url=URL('http://192.168.147.165:82/socket.io/?transport=polling&EIO=3&t=1687081526.5948737')



Conclusion:
As per socketio docs, it first establishes connection with the help of HTTP, then switches the protocol to websocket.
But ESP32 was not ready for that. Its on plain websockets.
"""