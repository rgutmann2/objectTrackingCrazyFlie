'''
Ryan Gutmann
ME 800: Object Tracking with CrazyFlie 2.1
Updated: 3/24/20
Object Detection Test
'''

'''
This code uses predetermined thresholds of HSV values
to detect a certain color. The thresholds set below are
for detecting the color red in the image. The code then 
determines which pixels are within the bounds and selects 
the largest continuous object and erases all other objects.
Then it places a bounding box around the largest object and 
shows the result.
'''


# Import required libraries
import cv2 as cv
import numpy as np
import time

# Import class for image processing
from image_process import imageProcess

def nothing(x):
    pass

# Create Object of the class imageProcess
ip = imageProcess()

# Upper and Lower Bounds for Finding Red
l_b = np.array([120,0,0])
u_b = np.array([180,255,255])

while True:
    # Read the test image
    frame = cv.imread('test.JPG')
    (height,width) = frame.shape[:2]
    width = int(width/2)
    height = int(height/2)
    cv.circle(frame,(width,height),5,(0,0,255),-1)

    # Convert colored image to HSV Image
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Generate Mask
    mask_in = cv.inRange(hsv, l_b, u_b)

    # Generate New Mask with a Single Blob
    mask_out = ip.select_largest_obj(mask_in)
    cv.imshow('mask_out',mask_out)

    # Draw Bounding Rectangle On mask_out
    x,y,w,h = cv.boundingRect(mask_out)
    cx = int(x + w/2)
    cy = int(y + h/2)
    cv.circle(frame,(cx,cy),10,(0,0,255),-1)
    cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
    cv.imshow("Frame",frame)

    time.sleep(0.5)

    key = cv.waitKey(1) & 0xFF
    if key == 27:
        break

cv.destroyAllWindows()
