"""
This file gets the camera feed from ESP32 via established websockets and feeds the caller.
"""
## for module-testing purpose, using webcam with opencv. After testing is done, actual feed will be linked
import cv2

vid = cv2.VideoCapture(0)

## Utitlities
def get_frames():
    """Gets the processed feed of camera

    Returns:
        _type_: _description_
    """
    while(True):
        
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
    
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
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    
        # # After the loop release the cap object
        # vid.release()
        # # Destroy all the windows
        # cv2.destroyAllWindows()
