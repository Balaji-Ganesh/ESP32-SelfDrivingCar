from app import create_app, socketio, esp32_comm, web_comm


# FIXME: later figure out the way to place this in some file like, `web` and `feed`
# alternative to socketio.on_event('manual_mode', handler=handle_manual_mode, namespace='/')

if __name__ == '__main__':
    # Establish communications..
    print("[DEBUG] main: About to establish communications")
    webapp = create_app()
    web_comm.init_communication(socketio)
    esp32_comm.init_communication(ip='192.168.0.165')
    from app.middleware.communication.web_communicator import *  # register event handlers
    print("[DEBUG] main: Communications established")

    print("[DEBUG] main: Starting the application...")
    web_comm.sock.run(webapp, debug=True)  # , host='0.0.0.0', port=port)
    print("[DEBUG] main: Thanks for utilizing the application.")
