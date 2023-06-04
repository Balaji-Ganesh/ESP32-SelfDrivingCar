"""
This script is the taken from the work done in "Rebuild-Self_Driving_car" repo 
    at "object_detection/COCO_mobilenet_ssd" folder.
"""

import cv2

# Load all the classes
classes = []  # to store all the classes
with open('../assets/model/labels.txt', 'rt') as file:
    classes = file.read().rstrip('\n').split('\n')
# print(classes)

# Configuration of the mobilenet model
configPath = '../assets/model/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = '../assets/model/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
# configurations as per docmentation --- find link
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def detectObjects(img, min_thresh=0.45, nms_thresh=0.2, draw_info=True, detectable_classes=[]):
    """
    @brief detects the objects* passed in `detectable_classes` with the given image.
    """
    # Send image to model to get prediction.
    classIds, confidences, bounding_boxes = net.detect(
        img, confThreshold=min_thresh,
        nmsThreshold=nms_thresh)  # consider if confidence is >50%, nms: Non max supressor (to avoid overlapping) - lower the value, the better.

    detection_info = []  # To return the info of objects detected.
    if len(bounding_boxes) > 0:  # When detected any object..
        # If user not passed any classes to be detected, then detect all classes, on which the model is trained.
        if len(detectable_classes) == 0:
            detectable_classes = classes

        # Overlay the prediction on the image..
        for classId, confidence, bbox in zip(classIds, confidences, bounding_boxes):
            detected_class = classes[int(classId) - 1]  # give as ..[class]
            # Detect only the objects to be detected, not all, on which the model is trained
            if detected_class in detectable_classes:
                detection_info.append((detected_class, bbox))
                if draw_info:  # Draw only if required..
                    cv2.rectangle(img, bbox, color=(0, 255, 0), thickness=2)
                    # print("id: ", classId)
                    cv2.putText(img, detected_class.upper(),
                                (bbox[0] + 5, bbox[1] + 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

    return img, detection_info


if __name__ == '__main__':
    # img = cv2.imread('lena.jpg')    # to work on saved image
    capture = cv2.VideoCapture(0)  # to work on real-time feed.
    # Set width and height of capturing..
    capture.set(3, 320)
    capture.set(4, 240)  # low frame size for faster computation.
    while True:
        _, img = capture.read()  # read the frames from camera
        img, detection_info = detectObjects(img, detectable_classes=['stop sign', 'traffic light', 'car',
                                                                     'truck'])  # !! Make sure that, classes names match with `labels.txt`
        print(detection_info)
        # Display output
        cv2.imshow('Output', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    capture.release()
    cv2.destroyAllWindows()
