"""
This file gets the processed output of the algorithm and sends it to the web-app.
"""
import asyncio
from multiprocessing import Process
# Event handlers for socketio


def handle_connect(self, ):
    print("[DEBUG] web: Client connected successfully")
    self.sock.send({'ack': "Connection established"})


def handle_disconnect(self, ):
    print("[DEBUG] web: Client disconnected successfully")
    self.sock.send({'ack': "Connection terminated."})


def handle_ack(self, data):
    print("[DEBUG] web: client's ack: ", data)


def stream_cam(self):
    # from .esp32_communicator import get_cam_feed
    from . import esp32_comm
    asyncio.get_event_loop().run_until_complete(esp32_comm.get_cam_feed())


def handle_stream(self, response):
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
    #         self.sock.emit('img_data', frame)
    #         self.sock.sleep(0)
    #     else:
    #         print("Can't stream ")
    #         break
    print("[DEBUG] web: Creating proceses to begin streaming")
    from . import web_comm
    camProcess = Process(target=web_comm.stream_cam)
    print("[DEBUG] web: about to start spawned process for streaming")
    camProcess.start()
    print("[DEBUG] web: Started spawned process for streaming")
    camProcess.join()
    print("[DEBUG] web: Streaming ended")
