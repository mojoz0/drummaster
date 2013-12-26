# create the wanted images
import cv
image=cv.LoadImage('picture.png', cv.CV_LOAD_IMAGE_COLOR)
grey=cv.CreateImage((100,100),8,1)
eig = cv.CreateImage (cv.GetSize (grey), 32, 1)
temp = cv.CreateImage (cv.GetSize (grey), 32, 1)
# the default parameters
quality = 0.01
min_distance = 10
# search the good points
features = cv.GoodFeaturesToTrack (
grey, eig, temp,
1000,
quality, min_distance, None, 3, 0, 0.04)
for (x,y) in features:
    x) + ',' + str(y)
cv.Circle (image, (int(x), int(y)), 3, (0, 255, 0), -1, 8, 0)


cv.ResetImageROI(image)
W,H=cv.GetSize(image)
w,h=cv.GetSize(template)
width=W-w+1
height=H-h+1
result=cv.CreateImage((width,height),32,1)
cv.MatchTemplate(frame,template, result,cv.CV_TM_SQDIFF)
(min_x,max_y,minloc,maxloc)=cv.MinMaxLoc(result)
(x,y)=minloc
cv.Rectangle(image2,(int(x),int(y)),(int(x)+w,int(y)+h),(255,255,255),1,0)