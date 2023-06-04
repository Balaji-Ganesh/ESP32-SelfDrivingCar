"""
This script is used to monitor the esp32 camera and pass controls as needed.
Takes help of utility scripts of "esp32cameraStreaming" and "navigateesp32"
"""
import cv2
import numpy as np
from utils.esp32camStream import *
from utils.navigateEsp32 import navigate, adjustSpeed

# ESP32 URL
URL = "http://192.168.232.165"  # Make sure to change at runtime

# Face recognition and opencv setup
cap = cv2.VideoCapture(URL + ":81/stream")

# For debugging
verbose_output=True

if __name__ == '__main__':
    # presets..
    set_resolution(URL, index=6)
    set_brightness(URL, value=1)
    set_led_intensity(URL, value=30)
    set_quality(URL, value=20)
    print("[INFO] Presets configured successfully")

    print("[INFO] Streaming starts..")
    while True:
        if cap.isOpened():
            ret, frame = cap.read()

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)

            cv2.imshow("frame", frame)

            key = cv2.waitKeyEx(1)
            
            # Adjusting Camera parameters at runtime..
            # NOTE: streaming pauses until is taken from user
            if key == ord('r'):
                idx = int(input("Select resolution index: "))
                set_resolution(URL, index=idx, verbose=True)

            elif key == ord('q'):
                val = int(input("Set quality (10 - 63): "))
                set_quality(URL, value=val)
            
            elif key == ord('b'):
                val = int(input("Set brightness (-2 - 2): "))
                set_quality(URL, value=val)
            
            elif key == ord('l'):
                val = int(input("Set led intensity (-2 - 2): "))
                set_led_intensity(URL, value=val)
            
            # Manual controls
            elif key == 56:     # numpad 8
                navigate(URL, "UP", verbose_output)
            elif key == 52:     # numpad 4
                navigate(URL, "LEFT", verbose_output)
            elif key == 54:     # numpad 6
                navigate(URL, "RIGHT", verbose_output)
            elif key == 50:     # numpad 5
                navigate(URL, "DOWN", verbose_output)
            elif key == 53:     # numpad 5
                navigate(URL, "STOP", verbose_output)
            elif key == 55:     # numpad 7 -- speed low by 10
                adjustSpeed(URL, -10, verbose_output)
            elif key == 57:     # numpad 9 -- speed up by 10
                adjustSpeed(URL, +10, verbose_output)
                
            # exit
            elif key == 27:
                break
                
            # elif key>-1:
            #     print(key)
    cv2.destroyAllWindows()
    cap.release()
