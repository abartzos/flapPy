# -*- coding: utf-8 -*-
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, time, random

#basic stuff
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
displayWidth = 600
displayHeight = 400
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
clock = pygame.time.Clock()
pygame.display.set_caption('flapPy')

#colors
black=(0,0,0)
white=(255,255,255)
darkGrey = (38, 39, 40)
grey = (130, 130, 130)
red = (255,0,0)
green = (0,255,0)
lightBlue = (85, 149, 252)

birdImg = pygame.image.load('images/bird.png')

def objectsCollide(obj1, obj2):
    obj1Rect = obj1.rect
    obj2Rect = obj2.rect
    return bool(obj1Rect.colliderect(obj2Rect))

class Pole(object):
    def __init__(self,color):
        self.color = color
    def display(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(gameDisplay, self.color, (x,y,w,h))

class Sprite(object):
    def __init__(self, image):
        self.image = image
    def display(self,x,y):
        self.x = x
        self.y = y
        dimensions = self.image.get_rect().size
        self.w = dimensions[0]
        self.h = dimensions[1]
        self.rect = pygame.Rect(x,y,self.w,self.h)
        gameDisplay.blit(self.image,(x,y))

class Game(object):
    def __init__(self):
        self.lost = False
        self.scoreInt = 0

        gameDisplay.fill(lightBlue)

        self.poleThickness = 30

        self.pole1Y = 0
        self.pole2Y = 300

        self.pole1H = 100
        self.pole2H = 100

        self.pole1 = None
        self.pole2 = None
        self.helpPole = None

        self.birdYChange = 0
        self.lost = False

        self.bird = Sprite(birdImg)
        self.birdY = int(displayHeight/2)
        self.birdX = 20 #(known bird x)
        self.birdYChange = 2

        self.bird.display(self.birdX,self.birdY)
        self.poleX = displayWidth - self.poleThickness

        self.displayNewPoles()

    def displayNewPoles(self):
        self.pole1 = Pole(green)
        self.pole2 = Pole(green)
        self.helpPole = Pole(green)

        self.pole2H = random.randint(100,200)
        self.pole1H = random.randint(100,200)

        self.poleGap = displayWidth - self.pole1H - self.pole2Y
        self.pole2Y = displayWidth - self.poleGap - self.pole1H

        self.pole1.display(self.poleX, self.pole1Y, self.poleThickness, self.pole1H)
        self.pole2.display(self.poleX, self.pole2Y, self.poleThickness, self.pole2H)
        self.helpPole.display(self.poleX, displayWidth - 50,self.poleThickness, displayWidth)

    def updatePoles(self):
        self.pole1.display(self.poleX, self.pole1Y, self.poleThickness, self.pole1H)
        self.pole2.display(self.poleX, self.pole2Y, self.poleThickness, self.pole2H)
        self.helpPole.display(self.poleX, displayHeight - 50, self.poleThickness, displayHeight)

    def jump(self):
        self.birdYChange = -10

    def hit(self):
        return self.lost

    def score(self):
        return self.scoreInt

    def frame(self):
        gameDisplay.fill(lightBlue)

        self.birdY += self.birdYChange
        self.bird.display(self.birdX,self.birdY)

        self.poleX -= 5

        self.updatePoles()

        if (self.birdY < 0 or self.birdY > displayHeight
        or objectsCollide(self.pole1, self.bird)
        or objectsCollide(self.pole2, self.bird)):
            self.lost = True
        if (self.bird.x == self.poleX
        and not objectsCollide(self.pole1, self.bird)
        and not objectsCollide(self.pole2,self.bird)
        and not objectsCollide(self.helpPole,self.bird)):
            self.scoreInt += 1
            self.poleX = displayWidth - self.poleThickness
            self.displayNewPoles()

        self.birdYChange = 2
        pygame.display.update()
        clock.tick(80)
