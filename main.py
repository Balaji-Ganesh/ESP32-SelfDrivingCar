import cv2
import base64
from app import socketio, app

# FIXME: later figure out the way to place this in some file like, `web` and `feed`
# alternative to socketio.on_event('manual_mode', handler=handle_manual_mode, namespace='/')


@socketio.on('manual_mode')
def handle_manual_mode(data):
    app.logger.info(data)
    print("Received data: "+str(data))
    # socketio.emit('acknowledgement', "You are connected")
    socketio.send('test')

# Event handlers for socketio
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected successfully")


if __name__ == '__main__':
    socketio.run(app, debug=True)
