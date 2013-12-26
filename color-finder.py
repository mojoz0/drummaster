#color-finder

import numpy
import cv

capture = cv.CaptureFromCAM(0)
imageSize = 1280, 720

h = 0
s = 0
v = 0

channels3 = cv.CreateImage(imageSize, 8, 3)
channels1 = cv.CreateImage(imageSize, 8, 1)

while True:
        frame = cv.QueryFrame(capture)
        clone = cv.CloneImage(frame)
        hsv = cv.CloneImage(channels3)
        threshold = cv.CloneImage(channels1)
        threshold2 = cv.CloneImage(channels1)
        
        cv.CvtColor(clone, hsv, cv.CV_BGR2HSV)
        cv.InRangeS(hsv, (110, 120, 75),
                    (140, 255, 255),
                   threshold)
        cv.InRangeS(hsv, (110, 120, 75),
                    (140, 255, 255),
                    threshold2)
        cv.Add(threshold, threshold2, threshold)
        cv.Erode(threshold, threshold, iterations = 5)
        cv.Dilate(threshold, threshold, iterations = 5)

        cv.ShowImage("normal", frame)

        cv.ShowImage("color", threshold)

        

 #       h += 1
        s += 1
        s %= 255
 #       v += 1
        
