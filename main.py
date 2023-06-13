from flask_socketio import SocketIO
from app import create_app
from app.middleware.communication import establish_communications

# FIXME: later figure out the way to place this in some file like, `web` and `feed`
# alternative to socketio.on_event('manual_mode', handler=handle_manual_mode, namespace='/')

if __name__ == '__main__':
    # Establish communications..
    print("[DEBUG] main: About to establish communications")
    webapp = create_app()
    socketio: SocketIO = SocketIO()
    establish_communications(webapp, socketio)
    print("[DEBUG] main: Communications established")
    
    from app.middleware.communication.web_communicator import *    # Register the event handlers

    print("[DEBUG] main: Starting the application...")
    socketio.run(webapp, debug=True)
    print("[DEBUG] main: Thanks for utilizing the application.")
