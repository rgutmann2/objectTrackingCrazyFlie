'''
Ryan Gutmann
ME 800: Object Tracking with CrazyFlie 2.1
Distance Control
Updated: 4/13/20
'''

'''
The following code uses information from the FPV camera to control
the altitude of the CrazyFlie in order to center the camera on the object.
'''

# Standard Library Imports
import cv2 as cv
import numpy as np
import time
import logging

# Third Party Imports
# from object_tracking.OpenCV.image_process import imageProcess
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from image_process import imageProcess

# Unique Radio Identifier
URI = 'radio://0/80/2M'

# Only Output Errors from the Logging Framework
logging.basicConfig(level=logging.ERROR)

# Initialize the Low-Level Drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)

# Create Instance of VideoCapture Class
cap = cv.VideoCapture(2)

# Create Instance of Image Processing Class
ip = imageProcess()

# Create Upper and Lower Bounds for HSV Values for the color Red
l_b = np.array([130,0,0])
u_b = np.array([180,255,255])

# Parameters for Altitude Control
tol_alt = 50

# Initialize Height
h = 0.4

# Center of Frame
c_frame_x = 320
c_frame_y = 240

with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
    cf = scf.cf

    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')
    time.sleep(2)

    for y in range(8):
        cf.commander.send_hover_setpoint(0, 0, 0, y / 20)
        time.sleep(0.05)

    while True:
        # Capture Image from FPV Camera
        _, frame = cap.read()

        # Draw Rectangle to Represent Tolerance
        cv.rectangle(frame,(270,190),(370,290),(0,255,0),2)

        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Generate Mask
        mask_in = cv.inRange(hsv, l_b, u_b)

	
        # Generate New Mask with a Single Blob
        mask_out = ip.select_largest_obj(mask_in)

        # Draw Bounding Rectangle
        x,y,w,h = cv.boundingRect(mask_out)
        cx = int(x + w/2)
        cy = int(y + h/2)
        cv.circle(frame,(cx,cy),2,(0,0,255),-1)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)

        # Forward Velocity
        if abs(c_frame_y - cy) >= tol_alt:
            if c_frame_y - cy >= 0:
                h = h - 0.05
            else:
                h = h + 0.05

        # Command Motion of CrazyFlie
        cf.commander.send_hover_setpoint(0,0,0,h)


        # Show Camera Feed
        cv.imshow("Frame",frame)
        
        time.sleep(0.05)

        key = cv.waitKey(1) & 0xFF
        if key == 27:
            break
        
    for y in range(8):
        cf.commander.send_hover_setpoint(0, 0, 0, (10 - y)/20)
        time.sleep(0.2)

    cf.commander.send_stop_setpoint()
    cap.release()
    cv.destroyAllWindows()
