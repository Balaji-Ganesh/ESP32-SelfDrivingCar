from app import create_app
import cv2
import time
socketio, app = create_app()

# FIXME: later figure out the way to place this in some file like, `web` and `feed`


def send_image():
    with open('640x480.jpg', 'rb') as f:
        image_data = f.read()
    socketio.emit('img_data', {'image': image_data})


is_img_recvd, is_conn_handshake_done, is_begin_stream = True, False, False


@socketio.on('ack')
def handle_acknowledge(response):
    """When received ack from client - that image has received, then send the next frame"""
    global is_img_recvd, is_conn_handshake_done, is_begin_stream
    if response['msg'] == 'CONN_ESTABLISHED':
        print("Connection Established")
        is_conn_handshake_done = True
    elif response['msg'] == 'BEGIN_STREAM':
        print("Start stream, recvd ack")
        is_begin_stream = True
    elif response['msg'] == 'IMG_YES':
        is_img_recvd = True
        print("Recvd ack from client. Send next frame")
    else:
        print('Unknown response received. Got '+str(response))


def stream_webcamera():
    global is_img_recvd
    # define a video capture object
    vid = cv2.VideoCapture(0)

    while True:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Now encode it to send over connection
        ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
        frame = buffer.tobytes()
        socketio.emit('img_data', {'image': frame})
        print("Sent image. Waiting for ack.")
        is_img_recvd = False
        if cv2.waitKey(1) == 27:
            break

        time.sleep(0.5)
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

# Event handlers for connection events


@socketio.on('connect')
def handle_connect():
    print("Client connected successfully")
    # send image data..
    if is_conn_handshake_done:
        print("Handshake successful")

@socketio.on('/stream')
def handle_stream():
    print("Waiting for ack - to begin stream")
    if is_begin_stream == True:
        print("Server about to send the image")
        input("Enter some key to send image")
        send_image()
        if input("Enter some key to begin stream") == 'y':
            stream_webcamera()
        print("Server sent the image")


@socketio.on('disconnect')
def handle_connect():
    print("Client connected successfully")

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