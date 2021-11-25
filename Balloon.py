#  Balloon class

import pygame
import random
from pygame.locals import *
import pygwidgets
from BalloonConstants import *

#
#  Balloon class
#

class Balloon():

    popSound = pygame.mixer.Sound('sounds/balloonPop.wav')
    smallBalloonImage = pygame.image.load('images/redBalloonSmall.png')
    mediumBalloonImage = pygame.image.load('images/redBalloonMedium.png')
    largeBalloonImage = pygame.image.load('images/redBalloonLarge.png')

    def __init__(self, window, maxWidth, maxHeight, ID):
        self.window = window
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.ID = ID
        self.size = random.choice(('Small', 'Medium', 'Large'))
        if self.size == 'Small':
            self.balloonImage = pygwidgets.Image(window, (0, 0), Balloon.smallBalloonImage)
            self.nPoints = 30
            self.speedY = 3.1
        elif self.size == 'Medium':
            self.balloonImage = pygwidgets.Image(window, (0, 0), Balloon.mediumBalloonImage)
            self.nPoints = 20
            self.speedY = 2.2
        else:  # large
            self.balloonImage = pygwidgets.Image(window, (0, 0), Balloon.largeBalloonImage)
            self.nPoints = 10
            self.speedY = 1.5
        self.setDetails()

    def setDetails(self):
        # Set a few details for this balloon
        balloonRect = self.balloonImage.getRect()
        self.width = balloonRect.width
        self.height = balloonRect.height

        # Position so that entire balloon is within the window
        self.x = random.randrange(self.maxWidth - self.width)
        self.y = self.maxHeight + random.randrange(100)
        self.balloonImage.setLoc((self.x, self.y))

    def clickedInside(self, mousePoint):
        # Returns two values:
        #  was the balloon clicked, number of points for the balloon
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if myRect.collidepoint(mousePoint):
            Balloon.popSound.play()
            return True, self.nPoints
        else:
            return False, 0

    def update(self):
        self.y = self.y - self.speedY   # update y position based on our speed
        self.balloonImage.setLoc((self.x, self.y))
        if self.y < -self.height:     # Off the top of the window
            return BALLOON_MISSED
        else:
            return BALLOON_MOVING

    def draw(self):
        self.balloonImage.draw()

    def __del__(self):
        print(self.size, 'Balloon with ID', self.ID, 'is going away')

class MegaBalloon(Balloon):
    squeakSound = pygame.mixer.Sound('sounds/balloonSqueak.wav')
    megaBalloonImage = pygame.image.load('images/megaBalloon.png')

    def __init__(self, window, maxWidth, maxHeight, ID):
        self.window = window
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.ID = ID
        self.balloonImage = pygwidgets.Image(window, (0, 0), MegaBalloon.megaBalloonImage)
        self.nPoints = 10
        self.speedY = 1.5
        self.clickCount = 0
        self.size = 'Mega'
        self.setDetails()

    def clickedInside(self, mousePoint):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if myRect.collidepoint(mousePoint):
            self.clickCount = self.clickCount + 1
            if self.clickCount == 3:
                Balloon.popSound.play()
                return True, self.nPoints
            else:
                MegaBalloon.squeakSound.play()
                return False, 0
        else:
            return False, 0