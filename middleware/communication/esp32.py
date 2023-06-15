import cv2
import websockets
import numpy as np
import logging

# The below functions will become data members of ESP32Manager in __init__.py


async def _connection_establisher(self):
    try:
        self.cam_ws = await websockets.connect(self.camera_ws_url)
        self.data_ws = await websockets.connect(self.data_ws_url)
    except Exception as e:
        logging.error(
            "[EXCEPTION] Connection establishment failed. Error: ", e)
    finally:
        logging.debug("Connection establishment done.")
    return 'ERROR in connection establishment'


async def _connection_terminater(self):
    try:
        # Close the connection
        await self.cam_ws.close()
        await self.data_ws.close()
        # Empty the connection holders
        self.cam_ws, self.data_ws = None, None
    except Exception as e:
        logging.error(
            "[EXCEPTION] Connection termination failed. Error: ", e)
    finally:
        logging.debug("Connection termination done.")
    return 'ERROR in connection termination'


async def _camera_client(self):
    try:
        # self.cam_ws = await websockets.connect(self.camera_ws_url)
        while True:
            msg = await self.cam_ws.recv()
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
        await self.cam_ws.close()
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
