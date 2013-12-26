# Trying shit out

import numpy
import cv


capture = cv.CaptureFromCAM(0)
image = cv.QueryFrame(capture)
temp = cv.CreateImage(cv.GetSize(image), 8, 3)

while True:
    frame = cv.QueryFrame(capture)
    cv.ConvertScale(frame, temp, 1.0, 0.5)
    cv.ShowImage("experiment", temp)
    cv.ShowImage("normal", frame)
    
