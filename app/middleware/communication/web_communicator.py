"""
This file gets the processed output of the algorithm and sends it to the web-app.
"""
from ..processor import read_feed
import cv2

def get_processed_frames():
    """Gets the processed feed of ESP32camera to display in web-app.
        - Feature Toggles can be used to adjust the features to be applied.
        #FIXME: Add the functionality to turn ON and OFF the features to be applied as required.
    Yields:
        cv2 image: processed camera image.
    """
    while(True):
        frame = read_feed()
    
        cv2.imshow("[DEBUG] Web-app", frame)
        print("web communicator ready to send frames")
        try:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print('[ERROR] An exception occured in sending frames')
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        # if cv2.waitKey(1) == 27:
        #     break
        # # Destroy all the windows
        # cv2.destroyAllWindows()