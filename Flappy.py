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

poleThickness = 30
poleX = displayWidth - poleThickness

pole1Y = 0
pole2Y = 300

pole1H = 100
pole2H = 100

pole1 = None
pole2 = None
helpPole = None

birdYChange = 0
score = 0
lost = False

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

def objectsCollide(obj1, obj2):
    obj1Rect = obj1.rect
    obj2Rect = obj2.rect
    return bool(obj1Rect.colliderect(obj2Rect))

def displayNewPoles():
    global poleGap, pole1H, pole2H, poleX, pole2Y
    global pole1, pole2, helpPole
    pole1 = Pole(green)
    pole2 = Pole(green)
    helpPole = Pole(green)

    pole2H = random.randint(100,200)
    pole1H = random.randint(100,200)

    poleGap = displayWidth - pole1H - pole2Y
    pole2Y = displayWidth - poleGap - pole1H

    pole1.display(poleX, pole1Y, poleThickness, pole1H)
    pole2.display(poleX, pole2Y, poleThickness, pole2H)
    helpPole.display(poleX, displayWidth - 50,poleThickness, displayWidth)

def updatePoles():
    global poleGap, pole1H, pole2H, poleX, pole2Y
    global pole1, pole2, helpPole

    pole1.display(poleX, pole1Y, poleThickness, pole1H)
    pole2.display(poleX, pole2Y, poleThickness, pole2H)
    helpPole.display(poleX, displayHeight - 50,poleThickness, displayHeight)


def jump():
    global birdYChange
    birdYChange = -10

def init():
    global poleGap, pole1H, pole2H, poleX, pole2Y, birdYChange
    global pole1, pole2, helpPole, birdY, bird, birdX
    # the values to be exported
    global lost, score

    lost = False
    score = 0

    gameDisplay.fill(lightBlue)

    displayNewPoles()
    bird = Sprite(birdImg)
    birdY = int(displayHeight/2)
    birdX = 20 #(known bird x)
    birdYChange = 2
    bird.display(birdX,birdY)

def frame():
    global poleGap, pole1H, pole2H, poleX, pole2Y, birdYChange
    global pole1, pole2, helpPole, birdY, bird, birdX
    # the values to be exported
    global lost, score

    gameDisplay.fill(lightBlue)

    birdY += birdYChange
    bird.display(birdX,birdY)

    poleX -= 5

    updatePoles()

    if (birdY < 0 or birdY > displayHeight or objectsCollide(pole1, bird) or objectsCollide(pole2, bird)):
        lost = True
    if (bird.x == poleX and not objectsCollide(pole1, bird)
    and not objectsCollide(pole2,bird)
    and not objectsCollide(helpPole,bird)):
        score += 1
        poleX = displayWidth - poleThickness
        displayNewPoles()

    birdYChange = 2
    pygame.display.update()
    clock.tick(80)