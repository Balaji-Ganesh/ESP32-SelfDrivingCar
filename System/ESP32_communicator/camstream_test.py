import websocket
import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Intial Configurations
ESP32_URL = '192.168.4.1'

## Presets
# choose the appropriate size - note that , this choice MUST match with ESP32 too.
IMG_X, IMG_Y = 320, 240 # VGA: 640x480, QVGA: 320x240

def decode_msg(msg):
    print("RECEIVED IMAGE")
    # print(msg)
    """ Decoding the image received """
    # A place holder to fill the binary image
    
    img_array = np.zeros(IMG_X, IMG_Y)  # !!! This size MUST match with ESP32 cam stream size.
    x, y, count = 0, 0, 0

    # Traverse the captured data one byte at a time and populate the image array
    for byte in bytearray(msg):
        y = count // IMG_X
        x = count % IMG_X
        img_array[y,x] = byte
        count += 1

    # display the captured image
    print("START")
    plt.figure('Capture Image 1')
    plt.imshow(img_array)
    plt.set_cmap('gray')
    plt.show(block=False)
    print("END")

# Helpers
count=0
def on_message(ws, msg):        # will be called, whenever the ESP32 sends feed on the registered namespace
    print("on msg called")
    binAnswer = ws.recv()
    # print(binAnswer)
    # print (websocket.ABNF.OPCODE_MAP[binAnswer.opcode])
 
    # for byte in bytearray(binAnswer.data):
    #     print( byte, "  ")
    print("on msg exited")

    

def on_open(ws, msg):
    print("System connected.")  # This will be sent to ESP32

def on_close(ws, msg):          # this will be called, when the connection closes.
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
