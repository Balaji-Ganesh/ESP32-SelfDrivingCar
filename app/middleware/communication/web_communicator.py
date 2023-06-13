"""
This file gets the processed output of the algorithm and sends it to the web-app.
"""
from . import socketio
import asyncio
from multiprocessing import Process

# Event handlers for socketio
@socketio.on('connect')
def handle_connect():
    print("[DEBUG] web: Client connected successfully")
    socketio.send({'ack': "Connection established"})

@socketio.on('disconnect')
def handle_disconnect():
    print("[DEBUG] web: Client disconnected successfully")
    socketio.send({'ack': "Connection terminated."})

@socketio.on('ack')
def handle_ack(data):
    print("[DEBUG] web: client's ack: ", data)

def stream_cam():
    from .esp32_communicator import get_cam_feed
    asyncio.get_event_loop().run_until_complete(get_cam_feed())

@socketio.on('stream')
def handle_stream(response):
    # Get the camera streamer..
    print("[DEBUG] web: (stream event) client sent: "+str(response))
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[STREAMING BEGINS]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    # cap = cv2.VideoCapture(0)
    # while (cap.isOpened()):
    #     ret, img = cap.read()
    #     if ret:
    #         img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #         frame = cv2.imencode('.jpg', img)[1].tobytes()
    #         frame = base64.encodebytes(frame).decode("utf-8")
    #         socketio.emit('img_data', frame)
    #         socketio.sleep(0)
    #     else:
    #         print("Can't stream ")
    #         break
    print("[DEBUG] web: Creating proceses to begin streaming")
    camProcess = Process(target=stream_cam)
    print("[DEBUG] web: about to start spawned process for streaming")
    camProcess.start()
    print("[DEBUG] web: Started spawned process for streaming")
    camProcess.join()
    print("[DEBUG] web: Streaming ended")