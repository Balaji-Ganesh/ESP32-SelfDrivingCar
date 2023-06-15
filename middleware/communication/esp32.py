import cv2
import websockets
import numpy as np
import logging

# The below functions will become data members of ESP32Manager in __init__.py


async def _camera_client(self):
    try:
        cam_ws = await websockets.connect(self.camera_ws_url)
        while True:
            msg = await cam_ws.recv()
            # even try with msg.data
            npimg = np.array(bytearray(msg), dtype=np.uint8)
            img = cv2.imdecode(npimg, -1)
            cv2.imshow("img", img)
            if cv2.waitKey(1) == 27:
                print('EXITING')
                cv2.destroyAllWindows()
                return 'Camera feed stopped by user'
    except Exception as e:
        logging.error(
            "[EXCEPTION] Camera streaming interrupted. Error: ", e)
    finally:
        await cam_ws.close()
        logging.debug("Camera Websockets Connection closed successfully")
    return 'ERROR in fetching feed'


async def _collision_dist_fetcher(self):
    async with websockets.connect(self.data_txrx_url) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

            # Process the message or perform any other task logic

            # response = f"Processed: {message}"
            # await websocket.send(response)
            # print(f"Sent response: {response}")
