import pygame
import os
import random
from pygame.locals import *
pygame.joystick.init()
#for every joystick pygame detects, make a new object/class
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
highscore_read = open('highscore.txt', "r")
contents = highscore_read.read()
ranthething = False
pygame.font.init()
pygame.init()
#window stuff
clock = pygame.time.Clock()
score = 0
cloudx = []
cloud = pygame.image.load("cloud.png")
raincloud = pygame.image.load("raincloud.png")
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("crow eat the worm")
crow = pygame.image.load("crow.png")
crowleft = pygame.image.load("crowleft.png")
idle = pygame.image.load("idle.png")
deadp = pygame.image.load("dead.png")
wormsprite = pygame.image.load("worm.png")
pygame.display.set_icon(crow)
playerx = 100
playery = 100
yvelocity = 0
direction = 2
wormx = random.randint(100, 400)
wormy = random.randint(100, 400)
gameovertext = pygame.image.load("gameover.png")
dead = False
for i in range(random.randint(1, 3)):
    cloudx.append(random.randint(80, 820))
def showscore():
    global direction
    global playery
    global yvelocity
    global contents
    global highscore_read
    global ranthething
    if direction != 2:
        playery += yvelocity
        yvelocity += 0.001
        if direction != 3:
            inter = pygame.font.Font('Inter-Medium.ttf', 30)
            txtsurface = inter.render('score: ' + str(score), True, (0, 0, 0))
            screen.blit(txtsurface, (10, 0))
        else:
            if ranthething == False and int(contents) < score:
                ranthething = True
                highscore_read.close()
                os.remove('highscore.txt')
                otherfile = open('highscore.txt', 'w')
                otherfile.write(str(score))
                contents = str(score)
            inter = pygame.font.Font('Inter-Medium.ttf', 40)
            intersmall = pygame.font.Font('Inter-Medium.ttf', 30)
            txtsurface = inter.render('Your Score: ' + str(score), True, (0, 0, 0))
            highscore_surface = intersmall.render('High Score: ' + contents, True, (0, 0, 0))
            screen.blit(txtsurface, (300, 270))
            screen.blit(highscore_surface, (350, 320))

                
def jump(force):
    global yvelocity
    yvelocity -= force
def player(x, y):
    global direction
    if direction == True:
        screen.blit(crow, (x,y))
    elif direction == 2:
        screen.blit(idle, (x,y))
    elif direction == False:
        screen.blit(crowleft, (x,y))
    else: 
        screen.blit(deadp, (400,190))
def worm(x, y):
    screen.blit(wormsprite, (x, y))
def collide(x1, y1, x2, y2):
    global score
    global wormx
    global wormy
    xdistance = x1 - x2
    ydistance = y1 - y2
    if ydistance > -60 and ydistance < 60 and xdistance > -60 and xdistance < 60:
        wormx = random.randint(70, 820)
        wormy = random.randint(70, 420)
        score += 1
        worm(wormx, wormy)
#main game loop
run = True
while run:
    for event in pygame.event.get():
        #the quitting window stuff
        if event.type == pygame.QUIT:
            pygame.font.quit()
            run = False
        if event.type == JOYBUTTONDOWN:
            if event.button == 2:
                #a button (controller)
                if direction != 2 and direction != 3:
                    jump()
            if event.button == 4:
                if direction == 3:
                    yvelocity = 0
                    direction = 2
                    playery = 100
                    playerx = 100
                    score = 0
                    dead = False
                    ranthething = False
        if event.type == JOYAXISMOTION:
            if event.joy == 0:
                #left joy stick
                if event.axis == 0 and event.value >= 0.4:
                    #right
                    if direction != 3:
                        playerx += 30
                        direction = True
                if event.axis == 0 and event.value <= -0.4:
                    #left
                    if direction != 3:
                        playerx -= 30
                        direction = False
                if event.axis == 1 and event.value <= -0.25:
                    #up
                    if direction != 2 and direction != 3:
                        jump(0.5)
        if event.type == JOYHATMOTION:
            #DPAD
            if event.value == (0, 1):
                if direction != 2 and direction != 3:
                    #up(controller)
                    jump(0.5)
            # if event.value == (0, -1):
            #     print('down')
            if event.value == (-1, 0):
                #left (controller)
                if direction != 3:
                    playerx -= 30
                    direction = False
            if event.value == (1, 0):
                #right (controller)
                   if direction != 3:
                    playerx += 30
                    direction = True
        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if direction != 2 and direction != 3:
                    jump(0.5)
            if event.key == pygame.K_RIGHT:
                if direction != 3:
                    playerx += 30
                    direction = True
            if event.key == pygame.K_LEFT:
                if direction != 3:
                    playerx -= 30
                    direction = False
            if event.key == pygame.K_r:
                if direction == 3:
                    yvelocity = 0
                    direction = 2
                    playery = 100
                    playerx = 100
                    score = 0
                    dead = False
                    ranthething = False
                    
    #fill screen
    screen.fill((73, 130, 208))
    if direction != 2 and direction != 3:
        for item in cloudx:
            screen.blit(cloud, (item, 20))
    if direction == 3:
        for item in cloudx:
            screen.blit(raincloud, (item, 20))
    if direction != 2 and direction != 3:
        worm(wormx, wormy)
        yvelocity += 0.001
    if playery > 580:
        direction = 3
        dead = True
    if direction == 3 and dead == True:
        screen.blit(gameovertext, (200, 90))
    showscore()
    for i in range(3):
        playery += yvelocity
    collide(playerx, playery, wormx, wormy)
    player(playerx, playery)
    # print(yvelocity)
    pygame.display.update()
    clock.tick(400)

