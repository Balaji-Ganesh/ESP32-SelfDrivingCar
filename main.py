from app import create_app

socketio, app = create_app()

#FIXME: later figure out the way to place this in some file like, `web` and `feed`

# Handle specific events -- client uses `emit` for these
@socketio.on('manual_mode') # alternative to socketio.on_event('manual_mode', handler=handle_manual_mode, namespace='/')
def handle_manual_mode(data):
    app.logger.info(data)
    print("Received data: "+str(data))
    # socketio.emit('acknowledgement', "You are connected")

    
# socketio.on_event('manual_mode', handler=handle_message, namespace='/')

# handle pre-defined events -- client uses `send` for these
@socketio.on('message')
def handle_message(data):
    print('client says: '+data)


if __name__ == '__main__':
    socketio.run(app, debug=True)