# -*- coding: utf-8 -*-
import pygame, time, random

a =1

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
swordSound = pygame.mixer.Sound('sounds/swordSound.wav')
coinSound = pygame.mixer.Sound('sounds/coin.wav')
punchSound = pygame.mixer.Sound('sounds/punch.wav')
pygame.mixer.music.load('music/Arcade.mp3')
gameLoopBool = True
startBool = True

poleThickness = 30
poleX = displayWidth - poleThickness

pole1Y = 0
pole2Y = 300 

pole1H = 100
pole2H = 100    

pole1 = None
pole2 = None
helpPole = None


def quitGame():
    pygame.quit()
    exit()
    
def textobjects(txt, font, color):
    textsurface = font.render(txt, True, color)
    return textsurface, textsurface.get_rect()

def textOrButton(txt,x,y,w,h,ic,ac,tc,font,bold,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        if click[0] ==1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
    smalltext = pygame.font.SysFont(font,20,bold)
    textsurf, textrect = textobjects(txt, smalltext, tc)
    textrect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textsurf, textrect)

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
    
    pole2H = random.randint(60, 100)
    pole1H = random.randint(50, 100) 
    
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

def displayNewEnemies(score):
    global balls, enemiesX, b1 ,b2, b3, b4
    enemiesX = displayWidth
    if score < 5:
        b1 = Ball(red)
        b2 = Ball(red)
        b1.display((enemiesX,random.randint(0,displayHeight)),20)
        b2.display((enemiesX,random.randint(0,displayHeight)),20)
        balls = 2
    elif score >= 5 and score <= 10:
        b1 = Ball(red)
        b2 = Ball(red)
        b3 = Ball(red)
        b1.display((enemiesX,random.randint(0,displayHeight)),20)
        b2.display((enemiesX,random.randint(0,displayHeight)),20)
        b3.display((enemiesX,random.randint(0,displayHeight)),20)
        balls = 3
    else:
        b1 = Ball(red)
        b2 = Ball(red)
        b3 = Ball(red)
        b4 = Ball(red)
        b1.display((enemiesX,random.randint(0,displayHeight)),20)
        b2.display((enemiesX,random.randint(0,displayHeight)),20)
        b3.display((enemiesX,random.randint(0,displayHeight)),20)
        b4.display((enemiesX,random.randint(0,displayHeight)),20)
        balls = 4

def updateEnemies():
    global balls, enemiesX, b1, b2, b3, b4
    if balls == 2:
        b1.display((enemiesX,b1.center[1]),20)
        b2.display((enemiesX,b2.center[1]),20)
    elif balls == 3:
        b1.display((enemiesX,b1.center[1]),20)
        b2.display((enemiesX,b2.center[1]),20)
        b3.display((enemiesX,b3.center[1]),20)
    elif balls == 4:
        b1.display((enemiesX,b1.center[1]),20)
        b2.display((enemiesX,b2.center[1]),20)
        b3.display((enemiesX,b3.center[1]),20)
        b4.display((enemiesX,b4.center[1]),20)

class Ball(object):
    def __init__(self,color):
        self.color = color
    def display(self,center,radius):
        #center is a tuple (x,y)
        #radius is a num
        self.center = center
        self.radius = radius
        self.bx = self.center[0] - self.radius
        self.by = self.center[1] - self.radius
        self.bw = self.radius * 2
        self.bh = self.radius *2
        self.rect = pygame.Rect(self.bx, self.by , self.bw, self.bh)
        pygame.draw.circle(gameDisplay, self.color, center, radius)

b1 = Ball(red)
b2 = Ball(red)
b3 = Ball(red)
b4 = Ball(red)

b1.display((-100,-100),20)
b2.display((-100,-100),20)
b3.display((-100,-100),20)
b4.display((-100,-100),20)

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

def startGame():
    pygame.mixer.music.play(-1)
    while startBool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(lightBlue)
        textOrButton('play',(displayWidth/2)-100,(displayHeight/2)-100,200,50,white,grey,black,'arial',True,gameLoop)
        textOrButton('quit',(displayWidth/2)-100,(displayHeight/2),200,50,white,grey,black,'arial',True,quitGame)
        
        pygame.display.update()
        clock.tick(60)

    
def gameLoop():
    global poleGap, pole1H, pole2H, poleX, pole2Y
    global pole1, pole2, helpPole, enemiesX, b1, b2, b3 ,b4

    gameDisplay.fill(lightBlue)
        
    score = 0    
    displayNewPoles()
    bird = Sprite(birdImg)
    birdY = int(displayHeight/2)
    birdX = 20 #(known bird width)
    birdYChange = 0
    bird.display(birdX,birdY)
    displayNewEnemies(0)
    
    while gameLoopBool:
        gameDisplay.fill(lightBlue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    birdYChange = -10
                    pygame.mixer.Sound.play(swordSound)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE: 
                    birdYChange = 2
            else:
                birdYChange = 2
        birdY += birdYChange
        bird.display(birdX,birdY)
        
        poleX -= 5
        enemiesX -=7
        
        updateEnemies()
        updatePoles()

        textOrButton(str(score),0,0,
             50,20,black,black,white,
             'arial',False,None
             )    
        if (birdY < 0 or birdY > displayHeight or objectsCollide(pole1, bird) 
        or objectsCollide(pole2,bird) or objectsCollide(b1,bird) or
        objectsCollide(b2,bird) or objectsCollide(b3,bird) or
        objectsCollide(b4, bird)):
            textOrButton('You Lose!',displayWidth/2-(displayWidth/4)/2,
                         displayHeight/2-(displayWidth/8)/2,
                         displayWidth/4,displayWidth/8,red,red,black,
                         'arial',True,None
                         )
            pygame.mixer.Sound.play(punchSound)
            pygame.display.update()
            for i in range(20000):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        quitGame()
                time.sleep(0.0001)
            gameLoop()
        if (bird.x == poleX and not objectsCollide(pole1, bird) 
        and not objectsCollide(pole2,bird)
        and not objectsCollide(helpPole,bird)
        and not objectsCollide(b1,bird)
        and not objectsCollide(b2,bird)
        and not objectsCollide(b3,bird)
        and not objectsCollide(b4,bird)):
            score += 1
            pygame.mixer.Sound.play(coinSound)
            poleX = displayWidth - poleThickness
            displayNewPoles()
            displayNewEnemies(score)

        pygame.display.update()
        clock.tick(70)

                                  
startGame()

