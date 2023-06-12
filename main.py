from app import create_app

socketio, app = create_app()

#FIXME: later figure out the way to place this in some file like, `web` and `feed`

def send_image():
    with open('640x480.jpg', 'rb') as f:
        image_data = f.read()
    socketio.emit('img_data', {'image': image_data})

# Event handlers for connection events
@socketio.on('connect')
def handle_connect():
    print("Client connected successfully");
    # send image data..
    print("Server about to send the image")
    send_image()
    print("Server sent the image")

@socketio.on('disconnect')
def handle_connect():
    print("Client connected successfully");

# Handle specific events -- client uses `emit` for these
@socketio.on('manual_mode') # alternative to socketio.on_event('manual_mode', handler=handle_manual_mode, namespace='/')
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