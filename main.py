import math
import random
import time
import pygame, sys
from pygame import mixer
mainClock = pygame.time.Clock()
from pygame.locals import *
import tkinter as tk
import datetime
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
clock=pygame.time.Clock()
# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
label="00:02:00"

font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
count = 7000
flag=True

# define the countdown func.
starImg = pygame.image.load('favourites.png')

def show_score(x, y):
    mins, secs = divmod(count, 60)
    timer = 'time left: {:02d}'.format(mins, )
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    if count<=1000:
        score1 = font.render(timer, True, (255, 0, 0))
    else:
        score1 = font.render(timer, True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(score1, (x+170, y))

def game_over_text():

    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    if score_value>=15 and score_value<20:
        screen.blit(starImg, (200,320))
    elif score_value>=20 and score_value<28:
        screen.blit(starImg, (200, 320))
        screen.blit(starImg, (265, 320))
    elif score_value >= 28 and score_value < 32:
        screen.blit(starImg, (200, 320))
        screen.blit(starImg, (265, 320))
        screen.blit(starImg, (340, 320))
    elif score_value >= 32 and score_value < 40:
        screen.blit(starImg, (200, 320))
        screen.blit(starImg, (265, 320))
        screen.blit(starImg, (340, 320))
        screen.blit(starImg, (405, 320))
    elif score_value >= 40:
        screen.blit(starImg, (200, 320))
        screen.blit(starImg, (265, 320))
        screen.blit(starImg, (340, 320))
        screen.blit(starImg, (405, 320))
        screen.blit(starImg, (470, 320))
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    if flag == True:
        count -= 1
        clock.tick(100)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440 or count<=0:
            for j in range(num_of_enemies):
                flag=False
                count=0
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    def textObject(text, font):
        textSurface = font.render(text,True,(255,255,255))
        return textSurface, textSurface.get_rect()


    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def button(msg,x,y,w,h,ic,ac,):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
        button_8 = pygame.Rect(x, y, w, h)


        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = textObject(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)
        return button_8

    click = False


    def options():
        running = True
        while running:
            screen.fill((0, 0, 0))

            draw_text('options', font, (255, 255, 255), screen, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            mainClock.tick(60)


    def main_menu():
        while True:

            screen.fill((0, 0, 0))
            draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

            mx, my = pygame.mouse.get_pos()
            if  button("Go", 150, 450, 100, 50, (255, 0, 0), (255, 0, 0)).collidepoint((mx, my)):
                if click:
                    options()

            if  button("Quit", 550, 450, 100, 50, (255, 255, 0), (255, 255, 0)).collidepoint((mx, my)):
                if click:
                    options()
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            mainClock.tick(60)

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()


