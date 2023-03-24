import cv2
from utils import preprocess, laneDetection
from moviepy.editor import VideoFileClip
import numpy as np
import imutils

# Camera calibration data
# Load the stored calibration matrices..
mtx = np.loadtxt('../assets/calibration/cameraMatrix.txt',
                 dtype='float', delimiter=',')
dist = np.loadtxt('../assets/calibration/cameraDistortion.txt',
                  dtype='float', delimiter=',')


def simple_pipeline(frame):
    """
    @brief: Just goes through the pipeline designed with printing log messages.
    NOTE
    ----
    `detail_pipeline()` also contains the same pipeline, but it shows additional 
    details of in-between process.
    ?? Why two functions then?
        - this one uses the single variable `frame` for all intermediary steps,
            memory will be utilized less as it gets replaced in each step.
        - whereas that, uses separate variables for each step, increasing the
            memory usage.
    Assumptions:
        - Camera is in the exact middle of the car (on top surface).
            - based on this, lane center is determined.
    """
    try:
        frame_copy = frame.copy()

        frame = cv2.undistort(frame, mtx, dist, None, None)
        print("[INFO] calibration done.")
        frame, invM = preprocess.warp(frame)
        print("[INFO] warping done.")
    #     frame = preprocess.grayscale(frame)
        # Try erode() to spread out the detected edges.
        frame = preprocess.apply_color_transform(frame)
        print("[INFO] pre-processing done.")
        frame, left_curverad, right_curverad = laneDetection.search_around_poly(
            frame)
        print("[INFO] lane detection process done.")
        frame = cv2.warpPerspective(
            frame, invM, (frame.shape[1], frame.shape[0]), flags=cv2.INTER_LINEAR)
        frame = cv2.addWeighted(frame, 0.3, frame_copy, 0.7, 0)

        # Add curvature and distance from the center
        curvature = (left_curverad + right_curverad) / 2
        car_pos = frame_copy.shape[1] / 2
        center = (abs(car_pos - curvature)*(3.7/650))/10
        curvature = 'Radius of Curvature: ' + str(round(curvature, 2)) + 'm'
        center = str(round(center, 3)) + 'm away from center'
        frame = cv2.putText(frame, curvature, (20, 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        frame = cv2.putText(frame, center, (20, 40),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        print("[INFO] annotation on frame done.")
    except Exception as e:
        print("[ERROR] ", e)
    return frame


def detail_pipeline(frame, f_cnt):
    """
    @brief: does the same work as of `simple_pipeline()` with detailing each step.
    NOTE
    ----
    - read the doc of `simple_pipeline()`for more info.
    - for unambiguity, each step's frame is named with that step name.
    """
    try:
        print(f"[INFO] Frame: {f_cnt}")
        original = frame.copy()
        frame_copy = frame.copy()

        undistorted = cv2.undistort(frame, mtx, dist, None, None)
        print("\t[INFO] calibration done.")
        warped, invM = preprocess.warp(undistorted)
        print("\t[INFO] warping done.")
    #     frame = preprocess.grayscale(frame)
        # Try erode() to spread out the detected edges.
        preprocessed = preprocess.apply_color_transform(warped)
        print("\t[INFO] pre-processing done.")
        lanes_detected, left_curverad, right_curverad = laneDetection.search_around_poly(
            preprocessed)
        print("\t[INFO] lane detection process done.")
        inv_warped = cv2.warpPerspective(
            lanes_detected, invM, (frame.shape[1], frame.shape[0]), flags=cv2.INTER_LINEAR)
        weighted = cv2.addWeighted(inv_warped, 0.3, frame_copy, 0.7, 0)

        # Add curvature and distance from the center
        curvature = (left_curverad + right_curverad) / 2
        car_pos = frame_copy.shape[1] / 2
        center = (abs(car_pos - curvature)*(3.7/650))/10
        curvature = 'Radius of Curvature: ' + str(round(curvature, 2)) + 'm'
        center = str(round(center, 3)) + 'm away from center'
        annotated = cv2.putText(weighted, curvature, (20, 20),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        annotated = cv2.putText(annotated, center, (20, 40),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        print("\t[INFO] annotation on frame done.")

        # Merge the frames to show detailed process..
        detailed = np.vstack((np.hstack((original, warped,  cv2.cvtColor(
            preprocessed, cv2.COLOR_GRAY2BGR))), np.hstack((lanes_detected, inv_warped, annotated))))
        return detailed
    except Exception as e:
        print("\t[ERROR] (in pipeline) ", e)
    return frame


def processFrames(infile, outfile):
    output = outfile
    clip = VideoFileClip(infile)
    processingClip = clip.fl_image(simple_pipeline)
    processingClip.write_videofile(output, audio=True)


def main_run_rec_video(infile, outfile):
    """ @brief: main function to work on recorded feed."""
    processFrames(infile, outfile)


def main_run_live(is_show_in_detail=False):
    """ @brief: main function to work on live."""
    capture = cv2.VideoCapture(0)
    frame_counter = 0
    while True:
        read_status, frame = capture.read()
        if read_status == False:
            break

        frame = imutils.resize(frame, width=320)
        pipeline_img = detail_pipeline(frame, frame_counter)
        frame_counter += 1
        cv2.imshow("Lane detection on Live feed", pipeline_img)

        if cv2.waitKey(1) & 0xFF == 27:
            fps = capture.get(cv2.CAP_PROP_FPS)
            print(f"[INFO] Total frames processed: {frame_counter}, Total time elapsed: {(frame_counter/fps)}s.")
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    choice = int(input("[INPUT] Choose the mode to run: \n\
                        1. To work on recorded feed\n\
                        2. To work on live feed\n\
                        choice: "))
    if (choice == 1):
        print("[INFO] Chosen Mode: Work on recorded feed.")
        print("[NOTE] Please re-check the path of recorded feed.")
        infile = "./../data/road_video_at_11h52m20s_forward_route.mp4"
        outfile = "./../data/road_video_at_11h52m20s_forward_route_output.mp4"
        main_run_rec_video(infile, outfile)
    elif (choice == 2):
        print("[INFO] Chosen Mode: Work on live feed.")
        choice = int(input("[INPUT] Choose the mode\n\
                    1. Show only final output\n\
                    2. Show detailed steps\n\
                    choice: "))
        if choice == 1:
            print("[INFO] Chosen Mode: Show only final output.")
            main_run_live(is_show_in_detail=True)
        elif choice == 2:
            print("[INFO] Chosen Mode: Show detailed steps.")
            main_run_live(is_show_in_detail=True)
        else:
            print("[ERROR] Incorrect mode chosen. Program quits. Bye.")
    else:
        print("[ERROR] Incorrect mode chosen. Program quits. Bye.")
