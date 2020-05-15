'''
Ryan Gutmann
ME 800: Object Tracking with CrazyFlie 2.1
Updated: 3/31/20
Camera Test with OpenCV
'''

'''
This code simply captures the video feed from 
a camera. Simply change the index in the input of
VideoCapture to choose a different camera.
'''

# Import OpenCV Library
import cv2

# Create instance of camera
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
