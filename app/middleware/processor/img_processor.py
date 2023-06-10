"""
This file gets the feed from the ESP32 and applies image processing algorithms on it.
Resultant output is set to accessible outside the script for displaying in web-app.
"""
from ..communication import get_cam_feed
import cv2

def read_feed():
    """This is dummy function for now.
    #FIXME: add image processing functionality in the next iteration.

    Yields:
        cv2 image: processed frame of ESP32
    """
    frame = get_cam_feed()
    cv2.imshow("[DEBUG] Image processor", frame)
    yield frame  # <<<<<<<<<<<<---- expose the frames to web-communicator.