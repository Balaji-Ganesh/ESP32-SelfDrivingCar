"""
This script is the modification of the work done in "Rebuild-Self_Driving_car" repo 
    at "object_detection/COCO_mobilenet_ssd" and
    "Miscellaneous/DistanceMeasurement" folders.

Brief
-----
- This script 
    - takes the help of helpers in utils.
    - detects traffic light and signs and
    - approximates the distance between them and camera.
"""
import cv2
from utils import detector
from utils import distanceMeasurer as measurer

# Initial setup..
min_threshold = 125     # min value to proceed for traffic light recognition


def annotateTrafficLightAndSigns(img):
    """
    Recognizes the traffic light and signs from the given image and
    approximates the distance between them and camera.
    @:param img: source image
    :returns the image with annotated traffic light recognition

    Notes
    -----
    Steps:
    """
    # Step-0: Detect traffic light
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # traffic_lights = classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    img, detection_info = detector.detectObjects(
        img, draw_info=False, detectable_classes=['traffic light', 'stop sign'])  # can more classes when needed.
    print(detection_info)
    # traffic_light_coords= detection_info[1]

    for class_name, bbox in detection_info:
        # print (detection)
        """ Initial setup """
        focal_len = measurer.initial_setup()    # Find the focal length
        # Widths of physical objects (of classes to be detected) in cm.
        # --- guess, this is not required. Analyze how WangZheng used.
        traffic_light_w = 1.3
        stop_sign_w = 5

        # Draw the bounding box around the detected object.
        x, y, w, h = bbox
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)

        """ Find the class and annotate the detected class """
        if class_name == 'traffic light':
            # later, annotate on the image
            print("[INFO] Detected traffic light")
            # Extract the RoI
            roi = gray_img[y + 10:y + h - 10, x + 10:x + w - 10]
            # Apply gaussian blur on the roi
            mask = cv2.GaussianBlur(roi, (25, 25), 0)
            # find the brightest spots
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

            if maxVal - minVal >= min_threshold:
                print("in process of recognition", end="  :::  ")
                test_img = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
                cv2.circle(test_img, maxLoc, 5, (0, 0, 255), 5)
                cv2.imshow("taffic light", test_img)
                # recognize which light is currently turned on..
                # !! Proceeding with assumption that, traffic light will be vertical.
                # `h` is the height of all 3 lights combined. `-30` -> calibration
                one_light_height = h/3 - 20
                if maxLoc[1] < one_light_height:
                    class_name += " - red"
                # Neglecting yellow for now.. any way no purpose assigned and also getting flickering issues in detecting.
                # elif one_light_height < maxLoc[1] < one_light_height*2:
                #     class_name += " - yellow"
                elif maxLoc[1] > one_light_height*2:
                    class_name += " - green"

        """ Find the distance of the detected-class. 
            - With this approach, even had multiple detected objects, can show of only one.
            - later modify to show at the detected area itself.
        """
        dist_approx = measurer.distance_finder(focal_len, obj_width_in_frame=w)
        # annotate the label names
        cv2.putText(frame, text="Class: ", org=(10, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    color=(180, 250, 200), fontScale=0.5, thickness=1)
        cv2.putText(frame, text="Distance: ", org=(10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    color=(180, 250, 200), fontScale=0.5, thickness=1)
        
        # fill the place holders.
        cv2.putText(frame, text=f"{class_name.upper()}", org=(60, 28),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    color=(180, 180, 200), fontScale=0.6, thickness=2)
        cv2.putText(frame, text=f"{round(dist_approx, 2)}cm", org=(85, 52),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    color=(180, 100, 200), fontScale=0.6, thickness=2)

        print("[INFO] Class: ", class_name.upper(),
              ", dist: ", dist_approx, "cm.")

    return img


if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    capture.set(3, 320)
    capture.set(4, 240)

    while True:
        _, frame = capture.read()
        annotated_img = annotateTrafficLightAndSigns(frame)

        # Show the results..
        cv2.imshow("Traffic light and signs recognition", annotated_img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    capture.release()
