# USING RGB

import cv

capture = cv.CaptureFromCAM(0)

while True:
    frame = cv.QueryFrame(capture)
    copy = cv.CloneImage(frame)
    frameSize = cv.GetSize(frame)
    red = cv.CreateImage(frameSize, 8, 1)
    green = cv.CreateImage(frameSize, 8, 1)
    blue = cv.CreateImage(frameSize, 8, 1)
    cv.Add(green, green, blue)
    cv.Sub(red, green, red)
    cv.Split(copy, red, green, blue, None)
    cv.ShowImage("Red", red)
    cv.ShowImage("Green", green)
    cv.ShowImage("Blue", blue)
    key = cv.WaitKey(11)
