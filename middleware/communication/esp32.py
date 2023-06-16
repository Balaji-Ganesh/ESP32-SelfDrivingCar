import cv2
import websockets
import numpy as np
import logging

# The below functions will become data members of ESP32Manager in __init__.py


async def _connection_establisher(self) -> bool:
    try:
        self.cam_ws = await websockets.connect(self.camera_ws_url)
        self.data_ws = await websockets.connect(self.data_txrx_url)
        return True
    except Exception as e:
        logging.error(
            "[EXCEPTION] Connection establishment failed. Error: ", e)
    finally:
        logging.debug("Connection establishment initiated.")
    return False


async def _connection_terminater(self) -> bool:
    try:
        # Close the connection
        await self.cam_ws.close()
        await self.data_ws.close()
        # Empty the connection holders
        self.cam_ws, self.data_ws = None, None
        return True
    except Exception as e:
        logging.error(
            "[EXCEPTION] Connection termination failed. Error: ", e)
    finally:
        logging.debug("Connection termination initiated.")
    return False


async def _camera_client(self) -> bool:
    try:
        while True:
            msg = await self.cam_ws.recv()
            # even try with msg.data
            npimg = np.array(bytearray(msg), dtype=np.uint8)
            img = cv2.imdecode(npimg, -1)
            cv2.imshow("img", img)
            if cv2.waitKey(1) == 27:
                print('camera task stopping..')
                cv2.destroyAllWindows()
                return True
    except Exception as e:
        logging.error(
            "[EXCEPTION] Camera streaming interrupted. Error: ", e)
    return False


async def _collision_dist_fetcher(self):
    try:
        while True:
            message = await self.data_ws.recv()
            print(f"Received message: {message}")

            # FIXME: Find way to send some status (True, False) -- like using some condition at While loop
            # Process the message or perform any other task logic

            # response = f"Processed: {message}"
            # await websocket.send(response)
            # print(f"Sent response: {response}")
    # as currently using forever loop, need to break using ctrl+c
    except KeyboardInterrupt:
        logging.info("Collision data fetching interrupted.")
        return True
    # if any other exceptions..
    except Exception as e:
        print("[EXCEPTION] data fetching failed. Error: ", e)
        logging.error("Collision data fetching interrupted. Error: ", e)
    return False
