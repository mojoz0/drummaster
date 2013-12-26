# experimenting-2

import numpy
import cv

capture = cv.CaptureFromCAM(0)
frame = cv.QueryFrame(capture)
imageSize = cv.GetSize(frame)
hsv = cv.CreateImage(imageSize, 8, 3)


def drawStuff():
    a = 100
    for i in xrange(0,255, 5): 
        b = 80
        for c in xrange(0,255, 5):
            frame = cv.QueryFrame(capture)
            #print "a is", str(a) +  ". b is", str(b) +". c is", str(c)
            cv.CvtColor(frame, hsv, cv.CV_RGB2HSV)
            cv.Circle(frame, (imageSize[0]/2, imageSize[1]/2), c,
                          (a, b, c), 8, 0)
            cv.ShowImage("Test", frame)
            key = cv.WaitKey(7)

def betterDrawStuff():
    a = 0
    b = 0
    c = 0
    while a < 255:
        while b < 255:
            while c < 255:
                frame = cv.QueryFrame(capture)
                #print "a is", str(a) +  ". b is", str(b) +". c is", str(c)
                cv.Circle(frame, (imageSize[0]/2, imageSize[1]/2), c,
                          (a, b, c,), 8, 0)
                cv.ShowImage("Test", frame)
                key  = cv.WaitKey(7)
                c += 1
                a += 1
                b += 1
            



drawStuff()
