"""
This file gets the processed output of the algorithm and sends it to the web-app.
"""
from app import socketio, get_cam_feed # get the established instance
import asyncio
# from ..processor import read_feed
import base64
import cv2

# Event handlers for socketio
@socketio.on('connect')
def handle_connect():
    print("Client connected successfully")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected successfully")

@socketio.on('stream')
def handle_stream(response):
    print("client sent: "+str(response))
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
    # asyncio.get_event_loop().run_until_complete(get_cam_feed(socketio))
    print("Streaming.........................................")
