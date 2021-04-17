import pygame
import random
import math

from pygame import mixer

# Initializing the pygame
pygame.init()

# Creating the window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('bg1.png')

# Background sound
mixer.music.load('mario.mp3')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption(" QUICK CODES ")
icon = pygame.image.load('mrbn.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('ufo2.png')
playerX = 365
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
    enemyImg.append(pygame.image.load('enemy1.png'))
    enemyX.append(random.randint(0, 735))  # Initialization points
    enemyY.append(random.randint(5, 150))
    enemyX_change.append(0.3)  # speed
    enemyY_change.append(40)

# bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet in currently moving
bulletImg = pygame.image.load('bullet2.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2.5  # Speed
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Functions
def player(x, y):
    screen.blit(playerImg, (x, y))


def showScore(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # RGB colors of bg screen
    screen.fill((255, 255, 255))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check wheather its right or left
        if event.type == pygame.KEYDOWN:
            # print("Another key is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('bs1.mp3')  # Bullet sound
                    bullet_sound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking the boundary of player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 20000

            game_over_text()
            break
            # over_sound = mixer.Sound('over1.mp3')  # Explosion sound
            # over_sound.play()



        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion1.mp3')  # Explosion sound
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)  # Initialization points
            enemyY[i] = random.randint(15, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()



