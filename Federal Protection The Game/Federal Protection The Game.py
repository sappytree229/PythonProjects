# Imports Modules
from struct import pack_into
from pygame.locals import RLEACCEL
import pygame
import sys
import os
import random
import time

#######################################################################
###Variables###

# Initializes Game
pygame.init()

# Colours
white = (255,255,255)
black = (0,0,0)
gray = (59,59,59)
yellow = (244,196,48)
blue = (4, 44, 59)
orange = (255, 165, 0)
red = (255, 0, 0)

#Game Screen Variables
width = 1600
height = 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Federal Protection: The Game')
font = pygame.font.Font('freesansbold.ttf', 16)

#Player X and Y
player_x = 0
player_y = 0

# Game variables
score = 0
speed = 5
sky = blue
fps = 60
timer = pygame.time.Clock()
value = 0
velocity = 0

#Movement Variables
y_change = 0
x_change = 0
gravity = 1

#Obstacles location
obstacles = [1000, 1450, 1800]
obstacle_speed = 5

#Game start and stop
active = False

# define a variable to control the main loop
running = True

####################################################################

# Scrolling background
class Background():
      def __init__(self):
            Cityimage = pygame.image.load('Cityscape.png')
            self.bgimage = pygame.transform.scale(Cityimage, (1800, 605))
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.rectBGimg.width

            self.moving_speed = 0
         
      def update(self):
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
             
      def render(self):
         screen.blit(self.bgimage, (self.bgX1, self.bgY1))
         screen.blit(self.bgimage, (self.bgX2, self.bgY2))

background = Background()

#########################################################################

class Road():
    def __init__(self):
        self.image = pygame.draw.rect(screen, gray, [0, 600, width, 200])
        self.image = pygame.draw.rect(screen, yellow, [0, 695, width, 5])
        self.image = pygame.draw.rect(screen, yellow, [0, 705, width, 5])

    def render(self):
        screen.blit(self.image)

road = Road()

#########################################################################

class Player():
      def __init__(self):
            truckimage = pygame.image.load('FedProTruck1.png')
            #self.bgimage = pygame.transform.scale(truckimage, (1800, 605))
            self.re
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.rectBGimg.width

            self.moving_speed = 0
             
      def render(self):
         screen.blit(self.bgimage, (self.bgX1, self.bgY1))
         screen.blit(self.bgimage, (self.bgX2, self.bgY2))
       
########################################################################
#### main loop ####

while running:
    timer.tick(fps)

    #Background, Sky, and Pavement
    screen.fill(sky)
    pavement = pygame.draw.rect(screen, gray, [0, 600, width, 200])
    paint = pygame.draw.rect(screen, yellow, [0, 695, width, 5])
    paint2 = pygame.draw.rect(screen, yellow, [0, 705, width, 5])
    background.update()
    background.render()

    if not active:
        instruction_text = font.render(f'Press Space Bar to Start', True, white)
        screen.blit(instruction_text, (140, 50))

        instruction_text2 = font.render(f'Use the side arrow keys to move left or right', True, white)
        screen.blit(instruction_text2, (340, 150))

        instruction_text3 = font.render(f'use the up arrow key to jump', True, white)
        screen.blit(instruction_text3, (340, 100))

    if active:
        #Display current score
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(score_text, (800, 50))
    
    player = Player()

    obstacle0 = pygame.draw.rect(screen, red, [obstacles[0], 670, 20, 60])
    obstacle1 = pygame.draw.rect(screen, orange, [obstacles[1], 750, 80, 30])
    obstacle2 = pygame.draw.rect(screen, blue, [obstacles[2], 670, 60, 60])

    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            running = False

        #Code to start the game    
        if event.type == pygame.KEYDOWN and not active:
            if event.key == pygame.K_SPACE:
                active = True
                player_x = 60
                obstacles = [1000, 1450, 1800]
                score = 0
                background.moving_speed = 1.75
    
        #Code for horizontal and lateral movement
        if event.type == pygame.KEYDOWN and active == True:
            if event.key == pygame.K_UP and y_change == 0:
                y_change = 18
        
            if event.key == pygame.K_RIGHT:
                x_change = 4
            if event.key == pygame.K_LEFT:
                x_change = -6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_LEFT:
                x_change = 0

    #Random obstacles generator AND collision detection
    for i in range(len(obstacles)):
        if active:
            obstacles[i] -= obstacle_speed
            if obstacles[i] < -20:
                obstacles[i] = random.randint(1820, 1870)

                #Score increases
                score += 1

            if player.colliderect(obstacle0) or player.colliderect(obstacle1) or player.colliderect(obstacle2):
                active = False
                background.moving_speed = 0

    #player screen restraints
    if 0 <= player_x <= 1760:
        player_x += x_change
    if player_x < 0:
        player_x = 0
    if player_x > 1800:
        player_x = 1800

    #Jump and Gravity Rules
    if y_change > 0 or player_y < 370:
        player_y -= y_change
        y_change -= gravity
    if player_y > 370:
        player_y = 370
    if player_y == 370 and y_change <0:
        y_change = 0

    pygame.display.flip()

pygame.quit()