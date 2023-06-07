import websocket
import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Intial Configurations
ESP32_URL = '192.168.4.1'

# Presets
# choose the appropriate size - note that , this choice MUST match with ESP32 too.
IMG_X, IMG_Y = 320, 240  # VGA: 640x480, QVGA: 320x240
# Helpers

count = 0


def base64_to_image(string):
    print("Received String: ")#, string, end="\n\n\n")
    # Decode the base64 data to bytes
    image_bytes = base64.decodebytes(base64_data)
    print("deocded")
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    print("cvted to np array")
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    print("deocded with cv2")
    cv2.imwrite("img_"+str(count)+'.jpeg', image)
    count += 1
    print("image written")
    return image


# will be called, whenever the ESP32 sends feed on the registered namespace
def on_message(ws, msg):
    cv2.imshow("Feed", base64_to_image(msg))
    cv2.waitKey(1)


def on_open(ws, msg):
    print("System connected.")  # This will be sent to ESP32


# this will be called, when the connection closes.
def on_close(ws, msg):
    print("[INFO] Websockets connection closed successfully.")


if __name__ == '__main__':

    # If ws:// doesn't work, try using wss://
    ws_camera_url = 'ws://'+ESP32_URL+'/Camera'

    # Establish websocket connection
    # websocket.enableTrace(True) # for debugging purpose. Can safely uncomment.
    ws = websocket.WebSocketApp(ws_camera_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close)
    ws.run_forever()    # Keep running..!!

"""
Challenge:
    - Getting feed from ESP32 to Python
    - Decoding the image


Another person looking for answer for same question:
https://reverseengineering.stackexchange.com/questions/26224/decoding-messages-sent-received-by-python-websocket-client
https://kite.trade/forum/discussion/1481/possibly-receiving-encrypted-websocket-binary-data-how-to-decrypt
"""
