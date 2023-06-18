import cv2
import websockets
import numpy as np
import logging
import base64
from fastapi import WebSocket

# The below functions will become data members of ESP32Manager in __init__.py


async def connection_establisher(self) -> bool:
    from . import ESP32Manager, StatusManager
    try:
        ESP32Manager.cam_ws = await websockets.connect(self.camera_ws_url)
        ESP32Manager.data_ws = await websockets.connect(self.data_txrx_url)
        ESP32Manager.conn_status = StatusManager.ESTABLISHED
        return True
    except Exception as e:
        logging.error(
            "[EXCEPTION] Connection establishment failed. Error: ", e)
    finally:
        logging.debug("Connection establishment initiated.")
    return False


async def _connection_terminater(self) -> bool:
    from . import ESP32Manager, StatusManager
    try:
        # Close the connection
        await ESP32Manager.cam_ws.close()
        await ESP32Manager.data_ws.close()
        ESP32Manager.conn_status = StatusManager.TERMINATED
        # Empty the connection holders
        ESP32Manager.cam_ws, ESP32Manager.data_ws = None, None
        return True
    except Exception as e:
        logging.error(
            "[EXCEPTION] Connection termination failed. Error: ", e)
    finally:
        logging.debug("Connection termination initiated.")
    return False


async def camera_client(self, to_web: bool = False, ws: WebSocket = None, ) -> bool:
    from . import ESP32Manager
    try:
        while True:
            msg = await ESP32Manager.cam_ws.recv()
            # even try with msg.data
            npimg = np.array(bytearray(msg), dtype=np.uint8)
            img = cv2.imdecode(npimg, -1)

            # if needed to send to web-client.. encode it..
            if to_web:
                logging.debug("Sending camera feed to web client")
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                frame = base64.encodebytes(frame).decode("utf-8")
                ws.send_bytes(frame)

            cv2.imshow("img", img)
            if cv2.waitKey(1) == 27:
                print('camera task stopping..')
                cv2.destroyAllWindows()
                return True
    except Exception as e:
        logging.error(
            "[EXCEPTION] Camera streaming interrupted. Error: ", e)
    return False


async def collision_dist_fetcher(self, to_web: bool = False, ws: WebSocket = None, ) -> bool:
    counter=0
    from . import ESP32Manager
    try:
        print("------------------ Collision data fetcher ------------------------------")
        while True:
            dist = int(await ESP32Manager.data_ws.recv())
            print(f"Received message: {dist}")

            # if need send to web-client..
            if to_web:
                print("Sending collision feed to web client")
                await ws.send_text(data=str(dist+counter))
            print("Fetching...", str(dist+counter))    
            counter+=1
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

