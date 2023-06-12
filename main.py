from app import create_app
import cv2
import time
import base64
socketio, app = create_app()

# FIXME: later figure out the way to place this in some file like, `web` and `feed`

@socketio.on('connect')
def handle_connect():
    print("Client connected successfully")\

@socketio.on('stream')
def handle_stream(response):
    print("client sent: "+str(response))
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[STREAMING BEGINS]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, img = cap.read()
        if ret:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame = base64.encodebytes(frame).decode("utf-8")
            socketio.emit('img_data', frame)
            socketio.sleep(0)
        else:
            print("Can't stream ")
            break


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected successfully")

# Handle specific events -- client uses `emit` for these


# alternative to socketio.on_event('manual_mode', handler=handle_manual_mode, namespace='/')
@socketio.on('manual_mode')
def handle_manual_mode(data):
    app.logger.info(data)
    print("Received data: "+str(data))
    # socketio.emit('acknowledgement', "You are connected")
    socketio.send('test')


# socketio.on_event('manual_mode', handler=handle_message, namespace='/')

# handle pre-defined events -- client uses `send` for these
@socketio.on('test')
def handle_message(data):
    print('client says: '+str(data))
    socketio.send("server sending data")


if __name__ == '__main__':
    socketio.run(app, debug=True)
