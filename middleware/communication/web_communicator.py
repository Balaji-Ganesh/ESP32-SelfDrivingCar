"""
This file gets the processed output of the algorithm and sends it to the web-app.
"""
import asyncio
from threading import Thread
# Event handlers for socketio
import cv2
import base64


def handle_connect(self, ):
    print("[DEBUG] web: Client connected successfully")
    self.sock.send({'ack': "Connection established"})


def handle_disconnect(self, ):
    print("[DEBUG] web: Client disconnected successfully")
    self.sock.send({'ack': "Connection terminated."})


def handle_ack(self, data):
    print("[DEBUG] web: client's ack: ", data)


def stream_cam(self):
    from .esp32_communicator import get_cam_feed
    # Stream from esp32  cam feed
    from . import esp32_comm
    print("------------------------------ object check ----------------------", hasattr(esp32_comm, 'cameraws'))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_cam_feed())
    
    # # Stream from webcam
    # # -- test: First, could able to stream the webcam or not? w/ a separate process or thread.
    # # With threading (after monkey patching), this way working.
    # cap = cv2.VideoCapture(0)
    # while (cap.isOpened()):
    #     ret, img = cap.read()
    #     if ret:
    #         cv2.imshow("img", img)
    #         img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #         frame = cv2.imencode('.jpg', img)[1].tobytes()
    #         frame = base64.encodebytes(frame).decode("utf-8")
    #         self.sock.emit('img_data', frame)
    #         self.sock.sleep(0)
    #         if cv2.waitKey(1) == 27:
    #             break
    #     else:
    #         print("Can't stream ")
    #         break
    # pass


def handle_stream(self, response):
    # Get the camera streamer..
    print("[DEBUG] web: (stream event) client sent: "+str(response))
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[STREAMING BEGINS]]]]]]]]]]]]]]]]]]]]]]]]]]]")

    print("[DEBUG] web: Creating proceses to begin streaming")
    from . import web_comm
    camThread = Thread(target=web_comm.stream_cam)
    print("[DEBUG] web: about to start spawned process for streaming")
    camThread.start()
    print("[DEBUG] web: Started spawned process for streaming")
    camThread.join()
    # web_comm.sock.start_background_task(web_comm.stream_cam) # ref: https://stackoverflow.com/a/62095829

    # A test -- whether could able to stream without creating separate process/thread or not.
    # Test result: This way (w/o any process or thread) is working
    # cap = cv2.VideoCapture(0)
    # while (cap.isOpened()):
    #     ret, img = cap.read()
    #     if ret:
    #         cv2.imshow("img", img)
    #         img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #         frame = cv2.imencode('.jpg', img)[1].tobytes()
    #         frame = base64.encodebytes(frame).decode("utf-8")
    #         self.sock.emit('img_data', frame)
    #         self.sock.sleep(0)
    #         if cv2.waitKey(1) == 27:
    #             break
    #     else:
    #         print("Can't stream ")
    #         break

    print("[DEBUG] web: Streaming ended")
