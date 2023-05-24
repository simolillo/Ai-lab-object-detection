import cv2 as cv
import numpy as np
import os
from PIL import Image
from time import time


# draw rectangles around the detected faces in the original frame
def draw_rectangle(rectangles,frame):
    updated_frame = frame
    for (x, y, w, h) in rectangles:
        updated_frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return updated_frame


# load the trained model
cascade_fanta = cv.CascadeClassifier('cascade/cascade.xml')

loop_time = time()
cap = cv.VideoCapture(0)

while(True):

    # get an updated image of the webcam
    ret, frame = cap.read()

     # Convert the frame to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    blurred_frame = cv.GaussianBlur(gray_frame, (5, 5), 0)

    adjusted_frame = cv.equalizeHist(blurred_frame)

    # do object detection
    rectangles = cascade_fanta.detectMultiScale(adjusted_frame, scaleFactor=1.5, minNeighbors=4)

    # draw the detection results onto the original image
    detection_image = draw_rectangle(rectangles, adjusted_frame)

    # display the images
    cv.imshow('Matches', detection_image)

    # debug the loop rate
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')