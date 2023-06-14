"""
This file uses established websocket communication between ESP32 and the system for 
exchanging stream of messages.
"""
# Library imports
import cv2
import numpy as np
import websockets
import logging
import base64


""" --------------- Utility functions ------------ """
"""***************************** Helper functions  *****************************"""
# camera_ws, data_ws  = "",  ""

# Camera related..


async def get_cam_feed():
    """This function with the established websocket, gets the cam feed form ESP32.

    Usage: Just call this function as like some generator in loop to get the feed.

    Yields:
        cv2 image: Frames sent by ESP32
    """
    logging.debug("esp32: Proceeding to begin stream from ESP32....")
    from . import web_comm, esp32_comm
    try:
        logging.debug("esp32: Stream begins from ESP32....")
        while True:
            msg = await esp32_comm.cameraws.recv()
            logging.debug("esp32: Received frame from esp32")
            # even try with msg.data
            npimg = np.array(bytearray(msg), dtype=np.uint8)
            # print(npimg)
            img = cv2.imdecode(npimg, -1)
            cv2.imshow("img", img)
            # send the image to web-app          -- encoding, do as did for the webcam
            # frame = cv2.imencode('.jpg', img)[1].tobytes()
            # frame = base64.encodebytes(frame).decode("utf-8")
            # web_comm.sock.emit('img_data', frame)
            # web_comm.sock.sleep(0)

            if cv2.waitKey(1) == 27:
                print('EXITING')
                break
    # except websockets.exceptions:
    #     logging.error(
    #         "esp32: Receiving frames error. Connection might have broken, please try again. \nerror: ", e)
    except Exception as e:
        print("Exception type: ", type(e))
        logging.error("esp32: error: ", e)
    finally:
        # await esp32_comm.cameraws.close()
        pass
