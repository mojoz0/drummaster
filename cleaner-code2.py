#cleaner-code2.py

import numpy
import cv
import pygame
import pygame.camera
import random

pygame.mixer.pre_init()
pygame.init()
pygame.camera.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

snare = pygame.mixer.Sound("E_SNARE_02.wav")
tom1 = pygame.mixer.Sound("tomtomdrum7.wav")
tom2 = pygame.mixer.Sound("tomtomdrum6.wav")
hihat = pygame.mixer.Sound("hihat22.wav")
synchNoise = pygame.mixer.Sound("cowbell9.wav")
based = pygame.mixer.Sound("01-Based-Is-How-You-Feel-Inside.wav")
over = pygame.mixer.Sound("vegetaover9000.wav")
bonzo = pygame.mixer.Sound("Led-Zeppelin-Coda-Bonzo's-Montreux.wav")
yyz = pygame.mixer.Sound("Rush-yyz.wav")

tom2Coords = (50, 400, 350, 600)
tom1Coords = (400, 500, 700, 700)
snareCoords = (700, 500, 1000, 700)
hihatCoords = (900, 200, 1250, 400)

# opencv stuff
CAMERA_INDEX = 0
capture = cv.CaptureFromCAM(CAMERA_INDEX)
sampleFrame = cv.QueryFrame(capture)
imageSize = cv.GetSize(sampleFrame)
imageSize = 1280, 720

# pygame stuff
screen = pygame.display.set_mode(imageSize, 0)
#camlist = pygame.camera.list_cameras()
#print camlist
#cam = pygame.camera.Camera(camlist[0], imageSize)
#cam.start()
#cam.set_controls(hflip = True, vflip = False)
#snapshot = pygame.surface.Surface(imageSize, 0, screen)






class Stick(object):
    def __init__(self, color):
        self.frame = cv.QueryFrame(capture)
        self.color = color
        self.imageSize = cv.GetSize(self.frame)
        self.channels3 = cv.CreateImage(self.imageSize, 8, 3)
        self.channels1 = cv.CreateImage(self.imageSize, 8, 1)
        if self.color == "red":
            self.hueRange = (110, 140, 110, 140)
        elif self.color == "blue":
            self.hueRange = (165, 180, 0, 15)
        self.rectPoints = (0, 0, 0, 0)
        self.last50Centers = [(0,0)]*50
        self.wasInSnare = False
        self.wasInTom1 = False
        self.wasInTom2 = False
        self.stillness = 0
        

        

    def findRectPoints(self, oldRectPoints):
        hueRange = self.hueRange
        clone = cv.CloneImage(self.frame)
        hsv = cv.CloneImage(self.channels3)
        threshold = cv.CloneImage(self.channels1)
        threshold2 = cv.CloneImage(self.channels1)
        
        cv.CvtColor(clone, hsv, cv.CV_RGB2HSV)
        cv.InRangeS(hsv, (hueRange[0], 80, 80), (hueRange[1], 255, 255),
                   threshold)
        cv.InRangeS(hsv, (hueRange[2], 80, 80), (hueRange[3], 255, 255),
                    threshold2)
        cv.Add(threshold, threshold2, threshold)
        cv.Erode(threshold, threshold, iterations = 5)
        cv.Dilate(threshold, threshold, iterations = 5)
        
 #       cv.ShowImage(self.color, threshold)

        memory = cv.CreateMemStorage(0)
        clone2 = cv.CloneImage(threshold)
        contours = cv.FindContours(clone2, memory,
                                   cv.CV_RETR_LIST,
                                   cv.CV_CHAIN_APPROX_SIMPLE,
                                   (0, 0) )
        if not contours:
            rectPoints = oldRectPoints
        else:
            rectPoints = cv.BoundingRect(contours)
        return rectPoints

    def findCenterRadius(self):
        self.rectPoints = self.findRectPoints(self.rectPoints)
        left, top, width, height = self.rectPoints
        center = (int(left + float(width)/2),
                  int(top + float(height)/2))
        radius = int(float(height)/2)
        return center, radius

    def drawBoundingCircle(self, frame):
        center, radius = self.findCenterRadius()
        if self.color == "red":
            circleColor = (0, 0, 255)
        elif self.color == "blue":
            circleColor = (255, 0, 0)
        cv.Circle(frame, center, radius,
                  circleColor , 8, 0)

    def appendCentersList(self):
        # Note: this is where I update the current center too
        self.center = self.findCenterRadius()[0]
        self.last50Centers.pop(0)
        self.last50Centers.append(self.center)

    def snareHit(self):
        center = self.center
        if self.inDrumZone(center, "snare"):
            if self.wasInSnare == False:
                self.wasInSnare = True
                return True
            else:
                return False
        else:
            self.wasInSnare = False
            return False

    def tom1Hit(self):
        center = self.center
        if self.inDrumZone(center, "tom1"):
            if self.wasInTom1 == False:
                self.wasInTom1 = True
                return True
            else:
                return False
        else:
            self.wasInTom1 = False
            return False

    def tom2Hit(self):
        center = self.center
        if self.inDrumZone(center, "tom2"):
            if self.wasInTom2 == False:
                self.wasInTom2 = True
                return True
            else:
                return False
        else:
            self.wasInTom2 = False
            return False

    def hihatHit(self):
        center = self.center
        if self.inDrumZone(center, "hihat"):
            if self.wasInHihat == False:
                self.wasInHihat = True
                return True
            else:
                return False
        else:
            self.wasInHihat = False
            return False


    def inDrumZone(self, center, drum):
        if drum == "tom2":
            if (center[0] > tom2Coords[0] and center[1] > tom2Coords[1] and
                center[0] < tom2Coords[2] and center[1] < tom2Coords[3]):
                return True
            else:
                return False
        elif drum == "tom1":
            if (center[0] > tom2Coords[0] and center[1] > tom2Coords[1] and
                center[0] < tom2Coords[2] and center[1] < tom2Coords[3]):
                return True
            else:
                return False
        elif drum == "snare":
            if (center[0] > snareCoords[0] and center[1] > snareCoords[1] and
                center[0] < snareCoords[2] and center[1] < snareCoords[3]):
                return True
            else:
                return False
        elif drum == "hihat":
            if (center[0] > hihatCoords[0] and center[1] > hihatCoords[1] and
                center [0] < hihatCoords[2] and center[1] < hihatCoords[3]):
                return True
            else:
                return False
            
        
    def playSounds(self):
        if self.snareHit():
            loudness = self.determineVolume()
            snare.set_volume(loudness)
            snare.play()
        elif self.tom1Hit():
            loudness = self.determineVolume()
            tom1.set_volume(loudness)
            tom1.play()
        elif self.tom2Hit():
            loudness = self.determineVolume()
            tom2.set_volume(loudness)
            tom2.play()
        elif self.hihatHit():
            loudness = self.determineVolume()
            hihat.set_volume(loudness)
            hihat.play()

    def determineVolume(self):
        delta = abs(self.last50Centers[-1][0] - self.last50Centers[-2][0])
        print delta
        volumeConstant = float(delta)/1
        if volumeConstant > 1.0:
            volumeConstant = 1.0
        return volumeConstant

    def hasBeenStill(self):
        recentXAverage = float(sum(self.last50Centers[40:][0]))/10
        recentYAverage = float(sum(self.last50Centers[40:][0]))/10
        noiseRangeX = (recentXAverage - 100, recentXAverage + 100)
        noiseRangeY = (recentYAverage - 100, recentYAverage + 100)
        if (self.center[0] > noiseRangeX[0] and self.center < noiseRangeX[1] and
            self.center[1] > noiseRangeY[0] and self.center > noiseRangeY[1]):
            self.stillness += 1
            print self.stillness
        if self.stillness == 10:
            self.stillness = 0
            return True
        else:
            return False
        
        

            

'''
class Drum(object):
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def hit(self, stickPos):
        if self.stickInZone(stickPos):
            if st
            self.play()

    def stickInZone(self, stickPos):
        if (stickPos[0] > self.left and stickPos[1] > self.top and
            stickPos[0] < self.right and stickPos[1] < self.bottom):
            return True
        else:
            return True

'''



def startApp():
    pygame.display.set_caption("DrumMaster 9000!")
    pygame.draw.rect(screen, (0, 0, 255),
                     (0, 0, imageSize[0], imageSize[1]))
    titleFont = pygame.font.SysFont("Cambria", 72)
    title = titleFont.render("DrumMaster 9000!", True, (0, 0, 0))
    subtextFont = pygame.font.SysFont("Cambria", 36)
    subtext1 = subtextFont.render("Press any other key to play DRUMZ!!@@11!", True,
                                  (0, 0, 0))
    subtext2 = subtextFont.render("Press 'h' for help.", True, (0, 0, 0))
    subtext3 = subtextFont.render("Press 1, 2, or 3 for inspiration.", True,
                                  (0, 0, 0))
    musicFont = pygame.font.SysFont("Cambria", 36)
    basedText = subtextFont.render("Based Is How You Feel Inside - BADBADNOTGOOD",
                                 True, (0, 0, 0))
    bonzoText = subtextFont.render("Bonzo's Montreux (Moby Dick) - Led Zeppelin",
                                 True, (0, 0, 0))
    nowPlaying = subtextFont.render("Now Playing:", True, (0, 0, 0))
    yyzText = subtextFont.render("YYZ - Rush", True, (0, 0, 0))
    screen.blit(title, (imageSize[0]*1/3, 100))
    screen.blit(subtext1, (imageSize[0]*1/3, 300))
    screen.blit(subtext2, (450, 200))
    screen.blit(subtext3, (410, 250))
    screen.blit(nowPlaying, (250, 500))
    over.play()
    songs = [based, bonzo, yyz]
    songTexts = [basedText, bonzoText, yyzText]
    randSong = random.randint(0, 2)
    screen.blit(songTexts[randSong], (imageSize[0]*1/3, 500))
    songs[randSong].play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.mixer.stop()
                    pygame.draw.rect(screen, (0, 0, 255), (420, 450, 700, 100))
                    screen.blit(basedText, (imageSize[0]*1/3, 500))
                    based.play()
                elif event.key == pygame.K_2:
                    pygame.mixer.stop()
                    pygame.draw.rect(screen, (0, 0, 255), (420, 450, 700, 100))
                    screen.blit(bonzoText, (imageSize[0]*1/3, 500))
                    bonzo.play()
                elif event.key == pygame.K_3:
                    pygame.mixer.stop()
                    pygame.draw.rect(screen, (0, 0, 255), (420, 450, 700, 100))
                    screen.blit(yyzText, (imageSize[0]*1/3, 500))
                    yyz.play()
                elif event.key == pygame.K_h:
                    runHelpScreen()
                else:
                    pygame.mixer.stop()
                    pygame.display.quit()
                    runVideo()
        pygame.display.flip()

def runHelpScreen():
    helpSurface = pygame.Surface((imageSize[0], imageSize[1]))
    #pygame.display.set_caption("DrumMaster 9000!")
    pygame.draw.rect(helpSurface, (0, 255, 0),
                     (0, 0, imageSize[0], imageSize[1]))
    helpFont = pygame.font.SysFont("Cambria", 48)
    helpTitle = helpFont.render("HALP SCREEN! :D", True, (0, 0, 0))
    helpSurface.blit(helpTitle, (400, 100))
    screen.blit(helpSurface, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
    
def runVideo():
    frameCount = 0
    snareHit = tom1Hit = tom2Hit = False
    redStick = Stick("red")
    blueStick = Stick("blue")
    

    i = 2
    
    while True:
        if i %2 == 0:
            frame = cv.QueryFrame(capture)
            
            redStick.drawBoundingCircle(frame)
            blueStick.drawBoundingCircle(frame)

            redStick.appendCentersList()
            blueStick.appendCentersList()

            redStick.playSounds()
            blueStick.playSounds()

            cv.Rectangle(frame, (tom1Coords[0], tom1Coords[1]),
                         (tom1Coords[2], tom1Coords[3]), (255, 0, 0), 0)

            cv.Rectangle(frame, (tom2Coords[0], tom2Coords[1]),
                         (tom2Coords[2], tom2Coords[3]), (0, 255, 0), 0)

            cv.Rectangle(frame, (snareCoords[0], snareCoords[1]),
                         (snareCoords[2], snareCoords[3]), (0, 0, 255), 0)

            cv.Rectangle(frame, (hihatCoords[0], hihatCoords[1]),
                         (hihatCoords[2], hihatCoords[3]), (125, 125, 0), 0)

            if redStick.hasBeenStill():
                synchNoise.play()

            #print redStick.stillness
            #print redStick.last50Centers
            #print blueStick.last50Centers

            #snapshot = cam.get_image(snapshot)
            #screen.blit(snapshot, (0,0))
            


    ##        for event in pygame.event.get():
    ##            if event.type == pygame.KEYDOWN:
    ##                if event.key == pygame.K_h:
    ##                    runHelpScreen()
    ##        
            cv.Flip(frame,frame, 1)
            cv.ShowImage("DrumMaster 9000!", frame)
            key = cv.WaitKey(7)
            if key == 27:
                break
            frameCount += 1

#runVideo()
startApp()
main()
            
