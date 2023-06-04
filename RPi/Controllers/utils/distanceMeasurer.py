"""
This script is the taken from the work done in "Rebuild-Self_Driving_car" repo 
    at "Miscellaneous/DistanceMeasurement" folder.
"""

import cv2
import numpy as np

""" Intial setup """
# Get the HSV values from ""objectDetectorByColorSpace.py""
lowerHSV = np.array([0, 104, 88])
higherHSV = np.array([255, 255, 255])

# actual values..
obj_offset_in_cm = 15  # Get from the ruler measurement - distance between the camera and target object
obj_width_in_cm = 3.7  # Get from the ruler measurement - calculate the object's width (!! of particular color, what measured earlier)
obj_width_in_px = 203  # Get from the ""objectDetectorByColorSpace.py""'s "Object Detection" window 198

def focal_length_finder(object_distance, obj_width, obj_width_in_ref_img):
    """
    Finds the focal length of the camera.
    :param object_distance: Distance of the target object placed exact straightly towards camera (at same base) (in cm)
    :param obj_width: width of the target object (in real) (in cm)
    :param obj_width_in_ref_img: width of the target object in the taken image (reference img)(in pixels)
    :return: calculated focal length of the camera
    """
    focal_length = (obj_width_in_ref_img * object_distance) / obj_width
    return focal_length

def object_width_finder(frame, minObjectAreaThresh=900):
    obj_width_px = 0
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Extract the object ONLY by its hsv values
    maskFrame = cv2.inRange(hsvFrame, lowerHSV, higherHSV)
    # Apply threshold, to get a good mask -- by ignoring object's noises..
    _, maskFrame = cv2.threshold(maskFrame, 254, 255, cv2.THRESH_BINARY)
    # Find contours in the mask.
    contours, _ = cv2.findContours(maskFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Draw the contours around the object.
    for contour in contours:
        # Apply filter to neglect noises having same color space as target object.
        if cv2.contourArea(contour) > minObjectAreaThresh:
            # Draw the contours..
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            obj_width_px = w    # Store the object's width

    return obj_width_px

def distance_finder(focal_length, obj_width_in_frame) :
    """
    Infers the distance of the object from the camera
    :param focal_length: calculated focal length
    :param object_offset: pre-measured distance between camera and object
    :param obj_width_in_frame: calculated width of object (dynamic)
    :return: inferred distance
    """
    distance_in_cm = (obj_width_in_cm * focal_length) / obj_width_in_frame
    return distance_in_cm

def initial_setup():
    """
    This function is solely specially for the purpose of `trafficLightAndSigns.py`.
    Previously, it used to be in the __main__ section.
    """
    focal_length = focal_length_finder(object_distance=obj_offset_in_cm, obj_width=obj_width_in_cm,
                                       obj_width_in_ref_img=obj_width_in_px)
    return focal_length

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    capture.set(3, 640)
    capture.set(4, 480)

    """ Initial Setup """
    focal_length = initial_setup()
    # print("Focal length: ", focal_length)

    while True:
        _, frame = capture.read()

        # Infer the object's distance
        obj_width_in_px_calc = object_width_finder(frame)    # Find the object's width in the frame
        if obj_width_in_px_calc != 0:
            object_distance_inf = distance_finder(focal_length, object_width_in_real=obj_width_in_cm,
                                                  obj_width_in_frame=obj_width_in_px_calc)
            cv2.putText(frame, text=f"Inferred object's distance: {object_distance_inf}cm\n"
                                    f" object's width: {obj_width_in_px_calc}px", org=(10, 40),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        color=(180, 250, 200), fontScale=0.5, thickness=1)
        # else:
        #     cv2.putText(frame, text="No target object to measure distance.", org=(10, 40),
        #                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #                 color=(0, 0, 200), fontScale=0.8, thickness=2)

        # Display the results
        cv2.imshow("Feed", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # resource release
    capture.release()
    cv2.destroyAllWindows()

"""
Ref: https://youtu.be/dBOqzLRgjtY
Correction to the bug got possible, by revisiting the basic concept from: https://youtu.be/Qm7vunJAtKY
Result:
Now working fairly accurate.
"""