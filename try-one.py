import numpy
import cv

# TERM PROJECT
'''
def detectStick(image):
    sticks = []
    detected = cv.
'''
    
CAMERA_INDEX = 0
capture = cv.CaptureFromCAM(CAMERA_INDEX)#
#cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)

def find_stick(frame):
    imageSize = cv.GetSize(frame)

    stick = cv.CreateImage(imageSize, 32, 1)
    red = cv.CreateImage(imageSize, 32, 1)
    hsv = cv.CreateImage(imageSize, 32, 3)
    sat = cv.CreateImage(imageSize, 32, 1)
    


i = 0

snare = False

while True:
    frame = cv.QueryFrame(capture)
    original = cv.CloneImage(frame)
    cv.ShowImage("Original", frame)
    imageSize = cv.GetSize(frame)
 #   stick = cv.CreateImage(imageSize, 32, 1)
    hsv = cv.CreateImage(imageSize, 8, 3)
##    red = cv.CreateImage(imageSize, 8, 1)
##    sat = cv.CreateImage(imageSize, 8, 1)
##    cv.Split(hsv, None, sat, None, None)
##    cv.Threshold(red, red, 128, 255, cv.CV_THRESH_BINARY)
##    cv.Threshold(sat, sat, 128, 255, cv.CV_THRESH_BINARY)
##    cv.Mul(red,sat,red)
##    cv.Erode(red, red, iterations = 5)
##    cv.Dilate(red,red, iterations = 5)
 #   cv.Smooth(original, hsv, cv.CV_BLUR, 7)
    cv.CvtColor(frame,hsv,cv.CV_RGB2HSV)
    cv.ShowImage("HSV", hsv)
    thresh = cv.CreateImage(imageSize, 8, 1)
    thresha = cv.CreateImage(imageSize, 8, 1)
    
    cv.InRangeS(hsv, (165,145,100), (140, 255, 255), thresh)
    cv.ShowImage("Modifieda", thresh)
    cv.InRangeS(hsv, (0,145,100), (10, 255, 255), thresha)
    cv.Add(thresh,thresha,thresh)
    
    cv.Erode(thresh, thresh, iterations=5)
    cv.Dilate(thresh, thresh, iterations=5)
##    cv.ShowImage("Saturated", sat)
##    cv.ShowImage("End Resul", red)    
    cv.ShowImage("Modified", thresh)
    memory = cv.CreateMemStorage(0)
    clone = cv.CloneImage(thresh)
    contours = cv.FindContours(clone, memory,
                                 cv.CV_RETR_LIST,
                                 cv.CV_CHAIN_APPROX_SIMPLE, (0, 0))
 #   cv.ShowImage("Only Contours", clone)
    cv.DrawContours(original, contours, 120, 0, 7)
    if not contours:
        rectPoints = (0,0,0,0)
    else:
        rectPoints = cv.BoundingRect(contours)
        #print rectPoints
        left, top, width, height = rectPoints
        right, bottom = left + width, top + height
        cv.Rectangle(original, (left, top), (right, bottom), 255, 9, 8, 0)
        if top > 500:
            if snare == False:
                print i
            snare = True
        else:
            snare = False

    cv.ShowImage("Contoured", original)
    
    key = cv.WaitKey(7)
    i += 1
