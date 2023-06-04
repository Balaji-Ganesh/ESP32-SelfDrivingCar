import cv2
import numpy as np

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def warp(img):
    w = img.shape[1]
    h = img.shape[0]

    src = np.float32([[9, 236], [98, 70], [217, 61], [317, 239]])
    dst = np.float32([[3, 238], [14, 5], [309, 2], [318, 238]])

    M = cv2.getPerspectiveTransform(src, dst)
    invM = cv2.getPerspectiveTransform(dst, src)

    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
#     print("test")

    return warped, invM

def abs_sobel_thresh(img, orient='x', thresh_min=25, thresh_max=255):
    # Convert to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS).astype(np.float)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    # Apply x or y gradient with the OpenCV Sobel() function
    # and take the absolute value
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(l_channel, cv2.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(l_channel, cv2.CV_64F, 0, 1))
    # Rescale back to 8 bit integer
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Create a copy and apply the threshold
    binary_output = np.zeros_like(scaled_sobel)
    # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    # Return the result
    return binary_output

def color_threshold(image, sthresh=(0,255), vthresh=(0,255)):
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    s_channel = hls[:,:,2]
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel > sthresh[0]) & (s_channel <= sthresh[1])] = 1

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    v_channel = hsv[:,:,2]
    v_binary = np.zeros_like(v_channel)
    v_binary[(v_channel > vthresh[0]) & (v_channel <= vthresh[1])] = 1

    output = np.zeros_like(s_channel)
    output[(s_binary == 1) & (v_binary) == 1] = 1

    # Return the combined s_channel & v_channel binary image
    return output

def s_channel_threshold(image, sthresh=(0,255)):
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    s_channel = hls[:, :, 2]  # use S channel

    # create a copy and apply the threshold
    binary_output = np.zeros_like(s_channel)
    binary_output[(s_channel >= sthresh[0]) & (s_channel <= sthresh[1])] = 1
    return binary_output

def apply_color_transform(img):
    #Apply Sobel operator in X-direction to experiment with gradient thresholds
    gradx = abs_sobel_thresh(img, orient='x', thresh_min=20, thresh_max=100)

    #Apply Sobel operator in Y-direction to experiment with gradient thresholds
    grady = abs_sobel_thresh(img, orient='y', thresh_min=20, thresh_max=100)

    #Experiment with HLS & HSV color spaces along with thresholds
    c_binary = color_threshold(img, sthresh=(100,255), vthresh=(50,255))
    
    #Combine the binary images using the Sobel thresholds in X/Y directions along with the color threshold to form the final image pipeline
    preprocessImage = np.zeros_like(img[:,:,0])
    preprocessImage[((gradx == 1) & (grady ==1) | (c_binary == 1))] = 255
    
    # Remove the noise and join the patches of road.
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(preprocessImage, kernel, iterations=1)
    dilated = cv2.dilate(preprocessImage, kernel, iterations=1)
    return dilated

def threshold(image):
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 220, 225, cv2.THRESH_BINARY)
    if(ret == False):
        print('Error in thresholding')
    else:
        return image

    """
9 ,  236
98 ,  70
217 ,  61
317 ,  239

    """