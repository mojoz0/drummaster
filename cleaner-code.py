#clean-code

import numpy
import cv
import pygame

pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

snare = pygame.mixer.Sound("E_SNARE_02.wav")


                         

CAMERA_INDEX = 0
capture = cv.CaptureFromCAM(CAMERA_INDEX)



def findPoints(frame, oldRectPoints):
    imageSize = cv.GetSize(frame)
    original = cv.CloneImage(frame)
    hsv = cv.CreateImage(imageSize, 8, 3)
    threshold = cv.CreateImage(imageSize, 8, 1)
    
    # Do things to the image to isolate the red parts

    cv.CvtColor(original, hsv, cv.CV_RGB2HSV)

    cv.InRangeS(hsv, (110, 80, 80), (140, 255, 255), threshold)
    cv.Erode(threshold, threshold, iterations = 5)
    cv.Dilate(threshold, threshold, iterations = 5)
    cv.ShowImage("shit", threshold)

    

    memory = cv.CreateMemStorage(0)
    clone = cv.CloneImage(threshold)
    contours = cv.FindContours(clone, memory,
                                cv.CV_RETR_LIST,
                                cv.CV_CHAIN_APPROX_SIMPLE, (0, 0))

 #   area = cv.ContourArea(contours)
    if not contours:
        # If there's no red on the screen
        rectPoints = oldRectPoints
    else:
        rectPoints = cv.BoundingRect(contours)
       # print rectPoints
        
    return rectPoints

    
        

rectPoints = (0,0,0,0)
frameCoint = 0
snareHit = False
            

while True:
    frame = cv.QueryFrame(capture)
    rectPoints = findPoints(frame, rectPoints)
    left, top, width, height = rectPoints
    right, bottom = left + width, top + height
    cv.Rectangle(frame, (100, 500), (500, 700), 120, -1, 8, 0)
    cv.Rectangle(frame, (left, top), (right, bottom), 255, 9, 8, 0)
    cv.Rectangle(frame, (left, top), (right, bottom), 255, 9, 8, 0)
    cv.Rectangle(frame, (left, top), (right, bottom), 255, 9, 8, 0)
    cv.ShowImage("Window", frame)
    if top > 500: # If stick is on drum
        if snareHit == False: # If stick was not on drum
            snare.play()
            snareHit = True
    else: # If stick is not on drum
        snareHit = False
    key = cv.WaitKey(7)
    i += 1

